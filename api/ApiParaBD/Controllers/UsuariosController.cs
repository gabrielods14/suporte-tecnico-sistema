using ApiParaBD.DTOs; // Necessário para os DTOs
using Microsoft.AspNetCore.Authorization; // Necessário para [Authorize]
using Microsoft.AspNetCore.Mvc; // Necessário para Controllers
using Microsoft.EntityFrameworkCore; // Necessário para operações assíncronas com o EF Core
using System.Security.Claims; // Necessário para ler o token

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

        // --- 1. CADASTRO (Padrão: PrimeiroAcesso = true) ---
        [AllowAnonymous]
        [HttpPost]
        public async Task<IActionResult> CriarUsuario([FromBody] CriarUsuarioDto usuarioDto)
        {
            if (await _context.Usuarios.AnyAsync(u => u.Email == usuarioDto.Email))
                return BadRequest(new { message = "E-mail já cadastrado." });

            var novoUsuario = new Usuario
            {
                Nome = usuarioDto.Nome,
                Email = usuarioDto.Email,
                SenhaHash = BCrypt.Net.BCrypt.HashPassword(usuarioDto.Senha),
                Telefone = usuarioDto.Telefone,
                Cargo = usuarioDto.Cargo,
                Permissao = usuarioDto.Permissao,
                PrimeiroAcesso = true // Força a troca de senha no primeiro login
            };

            _context.Usuarios.Add(novoUsuario);
            await _context.SaveChangesAsync();

            novoUsuario.SenhaHash = "";
            return CreatedAtAction(nameof(GetUsuario), new { id = novoUsuario.Id }, novoUsuario);
        }

        // --- 2. ADMIN EDITA QUALQUER USUÁRIO (Incluindo Senha) ---
        [Authorize(Roles = "Administrador")]
        [HttpPut("{id}")]
        public async Task<IActionResult> AdminAtualizarUsuario(int id, [FromBody] AtualizarUsuarioAdminDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound(new { message = "Usuário não encontrado." });

            // Atualiza dados básicos
            if (dto.Nome != null) usuario.Nome = dto.Nome;
            if (dto.Email != null) usuario.Email = dto.Email;
            if (dto.Telefone != null) usuario.Telefone = dto.Telefone;
            if (dto.Cargo != null) usuario.Cargo = dto.Cargo;
            if (dto.Permissao.HasValue) usuario.Permissao = dto.Permissao.Value;

            // Se o admin enviou uma nova senha, reseta a senha do usuário
            if (!string.IsNullOrEmpty(dto.NovaSenha))
            {
                usuario.SenhaHash = BCrypt.Net.BCrypt.HashPassword(dto.NovaSenha);
                // Opcional: Você pode definir PrimeiroAcesso = true aqui para forçar
                // o usuário a trocar essa senha que o admin definiu.
                usuario.PrimeiroAcesso = true; 
            }

            await _context.SaveChangesAsync();
            return Ok(new { message = "Usuário atualizado com sucesso." });
        }

        // --- 3. USUÁRIO TROCA A PRÓPRIA SENHA (Primeiro Acesso) ---
        [Authorize]
        [HttpPut("alterar-senha")]
        public async Task<IActionResult> AlterarMinhaSenha([FromBody] TrocarSenhaDto dto)
        {
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");
            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            // Verifica a senha atual
            if (!BCrypt.Net.BCrypt.Verify(dto.SenhaAtual, usuario.SenhaHash))
            {
                return BadRequest(new { message = "A senha atual está incorreta." });
            }

            // Define a nova senha
            usuario.SenhaHash = BCrypt.Net.BCrypt.HashPassword(dto.NovaSenha);
            
            // IMPORTANTE: Remove a flag de primeiro acesso
            usuario.PrimeiroAcesso = false;

            await _context.SaveChangesAsync();
            return Ok(new { message = "Senha alterada com sucesso!" });
        }

        // --- 4. USUÁRIO ATUALIZA O PRÓPRIO PERFIL ---
        [Authorize]
        [HttpPut("meu-perfil")]
        public async Task<IActionResult> AtualizarMeuPerfil([FromBody] AtualizarUsuarioDto dto)
        {
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");
            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            if (dto.Nome != null) usuario.Nome = dto.Nome;
            if (dto.Email != null) usuario.Email = dto.Email;
            if (dto.Telefone != null) usuario.Telefone = dto.Telefone;
            if (dto.Cargo != null) usuario.Cargo = dto.Cargo;

            await _context.SaveChangesAsync();
            return Ok(new { message = "Perfil atualizado." });
        }

        // --- 5. LEITURA E EXCLUSÃO (Padrão) ---
        [Authorize(Roles = "Administrador, SuporteTecnico")]
        [HttpGet]
        public async Task<IActionResult> GetUsuarios()
        {
            var usuarios = await _context.Usuarios.ToListAsync();
            foreach (var u in usuarios) u.SenhaHash = "";
            return Ok(usuarios);
        }

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
            var meuId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "0");
            if (id == meuId) return BadRequest(new { message = "Não pode excluir a si mesmo." });

            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound();

            _context.Usuarios.Remove(usuario);
            await _context.SaveChangesAsync();
            return NoContent();
        }
    }
}