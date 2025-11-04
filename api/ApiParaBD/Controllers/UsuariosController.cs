using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
// Adicione o using para a biblioteca de hashing
using BCrypt.Net;

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsuariosController : ControllerBase
    {
        private readonly AppContext _context;

        public UsuariosController(AppContext context)
        {
            _context = context;
        }

        // GET /api/Usuarios
        [HttpGet]
        public async Task<IActionResult> GetUsuarios()
        {
            // NOTA: Em um app real, crie um DTO de resposta para não expor a SenhaHash.
            var usuarios = await _context.Usuarios.ToListAsync();
            return Ok(usuarios);
        }

        // GET /api/Usuarios/5
        [HttpGet("{id}")]
        public async Task<IActionResult> GetUsuario(int id)
        {
            var usuario = await _context.Usuarios.FindAsync(id);

            if (usuario == null)
            {
                return NotFound();
            }

            return Ok(usuario);
        }

        // POST /api/Usuarios
        [HttpPost]
        public async Task<IActionResult> CriarUsuario([FromBody] CriarUsuarioDto usuarioDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            // --- HASHING DE SENHA IMPLEMENTADO ---
            // Gera um "sal" criptográfico e cria o hash da senha.
            string senhaHash = BCrypt.Net.BCrypt.HashPassword(usuarioDto.Senha);

            var novoUsuario = new Usuario
            {
                Nome = usuarioDto.Nome,
                Email = usuarioDto.Email,
                // Salva o hash seguro no banco de dados, nunca a senha original.
                SenhaHash = senhaHash,
                Telefone = usuarioDto.Telefone,
                Cargo = usuarioDto.Cargo,
                Permissao = usuarioDto.Permissao
            };

            _context.Usuarios.Add(novoUsuario);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetUsuario), new { id = novoUsuario.Id }, novoUsuario);
        }

        // PUT /api/Usuarios/5
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarUsuario(int id, [FromBody] AtualizarUsuarioDto usuarioDto)
        {
            var usuario = await _context.Usuarios.FindAsync(id);

            if (usuario == null)
            {
                return NotFound(new { message = "Usuário não encontrado." });
            }

            // Atualiza apenas os campos fornecidos (que não são null)
            if (usuarioDto.Nome != null)
            {
                usuario.Nome = usuarioDto.Nome;
            }
            if (usuarioDto.Email != null)
            {
                usuario.Email = usuarioDto.Email;
            }
            if (usuarioDto.Telefone != null)
            {
                usuario.Telefone = usuarioDto.Telefone;
            }
            if (usuarioDto.Cargo != null)
            {
                usuario.Cargo = usuarioDto.Cargo;
            }

            try
            {
                await _context.SaveChangesAsync();
                return Ok(new { message = "Perfil atualizado com sucesso!", user = usuario });
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!UsuarioExists(id))
                {
                    return NotFound(new { message = "Usuário não encontrado." });
                }
                else
                {
                    throw;
                }
            }
        }

        private bool UsuarioExists(int id)
        {
            return _context.Usuarios.Any(e => e.Id == id);
        }
    }
}

