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

        // --- 2. USUÁRIO TROCA A PRÓPRIA SENHA (Primeiro Acesso) ---
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

        // --- 3. USUÁRIO ATUALIZA O PRÓPRIO PERFIL ---
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

        // --- 4. LEITURA E EXCLUSÃO (Padrão) ---
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
        // --- 5. ADMIN ATUALIZA USUÁRIO POR ID (Incluindo Senha) ---
        [Authorize(Roles = "Administrador")]
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarUsuario(int id, [FromBody] AtualizarUsuarioAdminDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null)
            {
                return NotFound(new { message = "Usuário não encontrado." });
            }
            
            // Atualiza dados básicos (apenas se enviados)
            if (!string.IsNullOrEmpty(dto.Nome)) usuario.Nome = dto.Nome;
            if (!string.IsNullOrEmpty(dto.Email)) usuario.Email = dto.Email.ToLower();
            if (!string.IsNullOrEmpty(dto.Telefone)) usuario.Telefone = dto.Telefone;
            if (!string.IsNullOrEmpty(dto.Cargo)) usuario.Cargo = dto.Cargo;
            
            // Admin pode mudar permissão
            if (dto.Permissao.HasValue) usuario.Permissao = dto.Permissao.Value;

            // --- A LÓGICA INTELIGENTE DE SENHA ESTÁ AQUI ---
            // Só altera a senha se o admin enviou algo no campo 'NovaSenha'.
            // Se ele deixar vazio ou null no JSON, a senha antiga permanece intacta.
            if (!string.IsNullOrEmpty(dto.NovaSenha))
            {
                usuario.SenhaHash = BCrypt.Net.BCrypt.HashPassword(dto.NovaSenha);
                
                // Opcional: Se o admin trocou a senha, talvez queira forçar 
                // o usuário a trocá-la novamente no próximo login.
                usuario.PrimeiroAcesso = true; 
            }

            // Validação de e-mail duplicado (se o e-mail foi alterado)
            if (!string.IsNullOrEmpty(dto.Email))
            {
                 var emailExistente = await _context.Usuarios
                    .FirstOrDefaultAsync(u => u.Email == usuario.Email && u.Id != usuario.Id);
                 
                 if (emailExistente != null)
                 {
                     return BadRequest(new { message = "E-mail já está em uso por outra conta." });
                 }
            }

            await _context.SaveChangesAsync();
            
            usuario.SenhaHash = ""; // Não retorna o hash
            return Ok(new { message = "Usuário atualizado com sucesso.", usuario });
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