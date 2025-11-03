using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiParaBD.DTOs;
// Adicione o using para a biblioteca de hashing
using BCrypt.Net;

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
    }
}

