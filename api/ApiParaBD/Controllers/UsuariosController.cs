using ApiParaBD.DTOs;
using Microsoft.AspNetCore.Authorization; // Necessário para [Authorize]
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims; // Necessário para ler os dados do token

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsuariosController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public UsuariosController(ApplicationDbContext context)
        {
            _context = context;
        }

        // --- ENDPOINT DE CADASTRO (PÚBLICO) ---
        [AllowAnonymous] // Permite cadastro sem estar logado
        [HttpPost]
        public async Task<IActionResult> CriarUsuario([FromBody] CriarUsuarioDto usuarioDto)
        {
            // Verifica se o e-mail já existe
            if (await _context.Usuarios.AnyAsync(u => u.Email == usuarioDto.Email))
            {
                return BadRequest(new { message = "E-mail já cadastrado." });
            }

            var novoUsuario = new Usuario
            {
                Nome = usuarioDto.Nome,
                Email = usuarioDto.Email,
                // Hash da senha (segurança)
                SenhaHash = BCrypt.Net.BCrypt.HashPassword(usuarioDto.Senha),
                Telefone = usuarioDto.Telefone,
                Cargo = usuarioDto.Cargo,
                Permissao = usuarioDto.Permissao
            };

            _context.Usuarios.Add(novoUsuario);
            await _context.SaveChangesAsync();

            // Retorna o usuário criado, mas sem a senha hash
            novoUsuario.SenhaHash = ""; 
            return CreatedAtAction(nameof(GetUsuario), new { id = novoUsuario.Id }, novoUsuario);
        }

        // --- ENDPOINT: QUEM SOU EU? (PERFIL) ---
        // Este é o endpoint que resolve o problema da "Home" e do "Perfil"
        [Authorize] // Qualquer usuário logado pode acessar
        [HttpGet("meu-perfil")]
        public async Task<IActionResult> GetMeuPerfil()
        {
            // Pega o ID do usuário de dentro do Token JWT
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");

            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            usuario.SenhaHash = ""; // Segurança: não devolve a senha
            return Ok(usuario);
        }

        // --- ENDPOINT: ATUALIZAR MEU PRÓPRIO PERFIL ---
        [Authorize]
        [HttpPut("meu-perfil")]
        public async Task<IActionResult> AtualizarMeuPerfil([FromBody] AtualizarUsuarioDto dto)
        {
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");
            var usuario = await _context.Usuarios.FindAsync(userId);

            if (usuario == null) return NotFound();

            // Atualiza apenas os campos que foram enviados
            if (dto.Nome != null) usuario.Nome = dto.Nome;
            if (dto.Email != null) usuario.Email = dto.Email;
            if (dto.Telefone != null) usuario.Telefone = dto.Telefone;
            if (dto.Cargo != null) usuario.Cargo = dto.Cargo;

            await _context.SaveChangesAsync();
            
            usuario.SenhaHash = "";
            return Ok(usuario);
        }

        // --- ENDPOINT: LISTAR TODOS (SÓ ADMIN E SUPORTE) ---
        // Colaborador comum não deve ver a lista de todos os usuários
        [Authorize(Roles = "Administrador, SuporteTecnico")]
        [HttpGet]
        public async Task<IActionResult> GetUsuarios()
        {
            var usuarios = await _context.Usuarios.ToListAsync();
            foreach (var u in usuarios) u.SenhaHash = ""; // Limpa senhas
            return Ok(usuarios);
        }

        // --- ENDPOINT: BUSCAR POR ID (SÓ ADMIN E SUPORTE) ---
        [Authorize(Roles = "Administrador, SuporteTecnico")]
        [HttpGet("{id}")]
        public async Task<IActionResult> GetUsuario(int id)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound();
            usuario.SenhaHash = "";
            return Ok(usuario);
        }

        // --- ENDPOINT: ATUALIZAR USUÁRIO POR ID (SÓ ADMIN) ---
        [Authorize(Roles = "Administrador")]
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarUsuario(int id, [FromBody] AtualizarUsuarioDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound();

            // Verifica se o e-mail já existe em outro usuário
            if (dto.Email != null && dto.Email != usuario.Email)
            {
                if (await _context.Usuarios.AnyAsync(u => u.Email == dto.Email && u.Id != id))
                {
                    return BadRequest(new { message = "E-mail já cadastrado para outro usuário." });
                }
            }

            // Atualiza apenas os campos que foram enviados
            if (dto.Nome != null) usuario.Nome = dto.Nome;
            if (dto.Email != null) usuario.Email = dto.Email;
            if (dto.Telefone != null) usuario.Telefone = dto.Telefone;
            if (dto.Cargo != null) usuario.Cargo = dto.Cargo;
            if (dto.Permissao.HasValue) usuario.Permissao = dto.Permissao.Value;

            await _context.SaveChangesAsync();
            
            usuario.SenhaHash = "";
            return Ok(usuario);
        }

        // --- ENDPOINT: EXCLUIR USUÁRIO (SÓ ADMIN) ---
        [Authorize(Roles = "Administrador")]
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletarUsuario(int id)
        {
            // Impede que o admin se exclua a si mesmo por acidente
            var meuId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");
            if (id == meuId)
            {
                return BadRequest(new { message = "Você não pode excluir a sua própria conta enquanto está logado." });
            }

            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound();

            _context.Usuarios.Remove(usuario);
            await _context.SaveChangesAsync();

            return NoContent(); // 204 No Content (Sucesso)
        }
    }
}
