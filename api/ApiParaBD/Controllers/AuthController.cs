using ApiParaBD.DTOs;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        public AuthController(ApplicationDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDto loginRequest)
        {
            // Busca o usuário pelo e-mail fornecido, ignorando maiúsculas/minúsculas.
            var user = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email.ToLower() == loginRequest.Email.ToLower());

            // --- A CORREÇÃO ESTÁ AQUI ---
            // Se o usuário não for encontrado OU se a senha estiver incorreta,
            // retornamos o mesmo erro genérico. Isso evita que um atacante
            // saiba se o e-mail existe ou não no sistema ("enumeração de usuários").
            if (user == null || !BCrypt.Net.BCrypt.Verify(loginRequest.Senha, user.SenhaHash))
            {
                return Unauthorized(new { message = "E-mail ou senha inválidos." });
            }

            // Se chegou até aqui, as credenciais são válidas. Vamos gerar o token.
            var token = GenerateJwtToken(user);

            return Ok(new LoginResponseDto { Token = token });
        }

        private string GenerateJwtToken(Usuario user)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]!));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            // Os "claims" são as informações que queremos guardar dentro do token.
            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
                new Claim(JwtRegisteredClaimNames.Email, user.Email),
                new Claim("role", user.Permissao.ToString()) // Adicionamos a permissão do usuário
            };

            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.UtcNow.AddHours(8), // O token expira em 8 horas
                signingCredentials: credentials);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}