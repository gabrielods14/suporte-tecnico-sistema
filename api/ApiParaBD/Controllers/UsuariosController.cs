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
        // POST /api/Usuarios
        [AllowAnonymous] // Permite que qualquer um se cadastre
        [HttpPost]
        public async Task<IActionResult> CriarUsuario([FromBody] CriarUsuarioDto usuarioDto)
        {
            // (Lógica de hashing de senha e criação de usuário...)
            // ... (seu código existente de CriarUsuario) ...
            
            // Lógica de exemplo (assumindo que seu código existente está aqui)
            var usuarioExistente = await _context.Usuarios.FirstOrDefaultAsync(u => u.Email == usuarioDto.Email.ToLower());
            if (usuarioExistente != null)
            {
                return BadRequest(new { message = "E-mail já cadastrado." });
            }

            var novoUsuario = new Usuario
            {
                Nome = usuarioDto.Nome,
                Email = usuarioDto.Email.ToLower(),
                SenhaHash = BCrypt.Net.BCrypt.HashPassword(usuarioDto.Senha),
                Telefone = usuarioDto.Telefone,
                Cargo = usuarioDto.Cargo,
                Permissao = usuarioDto.Permissao
            };

            _context.Usuarios.Add(novoUsuario);
            await _context.SaveChangesAsync();

            // Ocultar a senha hash na resposta
            novoUsuario.SenhaHash = "[OCULTADO]"; 
            return CreatedAtAction(nameof(GetUsuarioPorId), new { id = novoUsuario.Id }, novoUsuario);
        }

        // --- ENDPOINT PARA LISTAR USUÁRIOS (ADMIN E SUPORTE) ---
        // GET /api/Usuarios
        [Authorize(Roles = "Administrador, SuporteTecnico")] // Só Admin e Suporte podem ver a lista
        [HttpGet]
        public async Task<IActionResult> GetUsuarios()
        {
            var usuarios = await _context.Usuarios.ToListAsync();
            // Ocultar todas as senhas hash
            usuarios.ForEach(u => u.SenhaHash = "[OCULTADO]");
            return Ok(usuarios);
        }

        // --- ENDPOINT PARA BUSCAR UM USUÁRIO (ADMIN E SUPORTE) ---
        // GET /api/Usuarios/5
        [Authorize(Roles = "Administrador, SuporteTecnico")]
        [HttpGet("{id}")]
        public async Task<IActionResult> GetUsuarioPorId(int id)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null)
            {
                return NotFound();
            }
            usuario.SenhaHash = "[OCULTADO]";
            return Ok(usuario);
        }

        // --- NOVO ENDPOINT: ATUALIZAR O PRÓPRIO PERFIL (QUALQUER USUÁRIO LOGADO) ---
        // PUT /api/Usuarios/meu-perfil
        [Authorize] // Qualquer usuário logado (Admin, Suporte, Colaborador)
        [HttpPut("meu-perfil")]
        public async Task<IActionResult> AtualizarMeuPerfil([FromBody] AtualizarUsuarioDto dto)
        {
            // Pegamos o ID do usuário A PARTIR DO TOKEN JWT
            var userIdString = User.Identity?.Name;
            if (string.IsNullOrEmpty(userIdString))
            {
                return Unauthorized(); // Token inválido ou não encontrado
            }

            var userId = int.Parse(userIdString);
            var usuario = await _context.Usuarios.FindAsync(userId);

            if (usuario == null)
            {
                return NotFound(new { message = "Usuário não encontrado." });
            }

            // Atualiza apenas os campos fornecidos
            if (!string.IsNullOrEmpty(dto.Nome)) usuario.Nome = dto.Nome;
            if (!string.IsNullOrEmpty(dto.Email)) usuario.Email = dto.Email.ToLower();
            if (!string.IsNullOrEmpty(dto.Telefone)) usuario.Telefone = dto.Telefone;
            if (!string.IsNullOrEmpty(dto.Cargo)) usuario.Cargo = dto.Cargo;
            
            // Verifica se o e-mail (se alterado) já existe
            var emailExistente = await _context.Usuarios.FirstOrDefaultAsync(u => u.Email == usuario.Email && u.Id != usuario.Id);
            if (emailExistente != null)
            {
                return BadRequest(new { message = "E-mail já está em uso por outra conta." });
            }

            await _context.SaveChangesAsync();
            usuario.SenhaHash = "[OCULTADO]";
            return Ok(usuario);
        }

        // --- NOVO ENDPOINT: ATUALIZAR QUALQUER USUÁRIO (SÓ ADMIN) ---
        // PUT /api/Usuarios/5
        [Authorize(Roles = "Administrador")] // Só Admin pode fazer isso
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarUsuario(int id, [FromBody] AtualizarUsuarioDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null)
            {
                return NotFound(new { message = "Usuário não encontrado." });
            }
            
            // Admin pode atualizar tudo
            if (!string.IsNullOrEmpty(dto.Nome)) usuario.Nome = dto.Nome;
            if (!string.IsNullOrEmpty(dto.Email)) usuario.Email = dto.Email.ToLower();
            if (!string.IsNullOrEmpty(dto.Telefone)) usuario.Telefone = dto.Telefone;
            if (!string.IsNullOrEmpty(dto.Cargo)) usuario.Cargo = dto.Cargo;

            // Lógica de verificação de e-mail (separada da atualização de perfil)
            if (!string.IsNullOrEmpty(dto.Email))
            {
                 var emailExistente = await _context.Usuarios.FirstOrDefaultAsync(u => u.Email == usuario.Email && u.Id != usuario.Id);
                 if (emailExistente != null)
                 {
                     return BadRequest(new { message = "E-mail já está em uso por outra conta." });
                 }
            }

            await _context.SaveChangesAsync();
            usuario.SenhaHash = "[OCULTADO]";
            return Ok(usuario);
        }
        
        // --- NOVO ENDPOINT: EXCLUIR UM USUÁRIO (SÓ ADMIN) ---
        // DELETE /api/Usuarios/5
        [Authorize(Roles = "Administrador")] // Só Admin pode fazer isso
        [HttpDelete("{id}")]
        public async Task<IActionResult> ExcluirUsuario(int id)
        {
            // Verifica se o Admin está tentando se auto-excluir
            var userIdString = User.Identity?.Name;
            if (id == int.Parse(userIdString ?? "0"))
            {
                return BadRequest(new { message = "Um administrador não pode excluir a própria conta." });
            }

            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null)
            {
                return NotFound(new { message = "Usuário não encontrado." });
            }

            // (Lógica de segurança adicional: verificar se o usuário a ser excluído é o último admin)
            if (usuario.Permissao == PermissaoUsuario.Administrador)
            {
                 var totalAdmins = await _context.Usuarios.CountAsync(u => u.Permissao == PermissaoUsuario.Administrador);
                 if (totalAdmins <= 1)
                 {
                     return BadRequest(new { message = "Não é possível excluir o último administrador do sistema." });
                 }
            }

            _context.Usuarios.Remove(usuario);
            await _context.SaveChangesAsync();

            return NoContent(); // Retorna 204 No Content (sucesso)
        }
    }
}
