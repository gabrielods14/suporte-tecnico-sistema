# 📋 Código Fonte das Classes CRUD - API C# .NET

Este documento contém o código fonte completo de todas as classes que realizam operações CRUD (Create, Read, Update, Delete) na API de Suporte Técnico desenvolvida em C# .NET 9.0.

---

## 📁 Estrutura do Projeto

```
ApiParaBD/
├── Controllers/          # Controladores REST (Endpoints)
│   ├── ChamadosController.cs
│   ├── UsuariosController.cs
│   ├── AuthController.cs
│   └── HealthCheckController.cs
├── Models/              # Modelos de Dados (Entidades)
│   ├── Usuario.cs
│   ├── Chamado.cs
│   └── HistoricoChamado.cs
├── DTOs/                # Data Transfer Objects
│   ├── CriarChamadoDto.cs
│   ├── AtualizarChamadoDto.cs
│   ├── CriarUsuarioDto.cs
│   ├── AtualizarUsuarioDto.cs
│   ├── LoginDto.cs
│   └── LoginResponseDto.cs
├── ApplicationDbContext.cs  # Contexto do Entity Framework
└── Program.cs           # Configuração da Aplicação
```

---

## 🔐 1. CONTROLLER DE AUTENTICAÇÃO (AuthController.cs)

### Responsabilidade: Gerenciar autenticação e geração de tokens JWT

```csharp
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
```

**Endpoints:**
- `POST /api/Auth/login` - Realiza login e retorna token JWT

---

## 👥 2. CONTROLLER DE USUÁRIOS (UsuariosController.cs)

### Responsabilidade: CRUD completo de usuários

```csharp
using ApiParaBD.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;

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
            var usuarioExistente = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email == usuarioDto.Email.ToLower());
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
        [Authorize(Roles = "Administrador, SuporteTecnico")]
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
            var emailExistente = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email == usuario.Email && u.Id != usuario.Id);
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
        [Authorize(Roles = "Administrador")]
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

            // Lógica de verificação de e-mail
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
            usuario.SenhaHash = "[OCULTADO]";
            return Ok(usuario);
        }
        
        // --- NOVO ENDPOINT: EXCLUIR UM USUÁRIO (SÓ ADMIN) ---
        // DELETE /api/Usuarios/5
        [Authorize(Roles = "Administrador")]
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

            // Verificar se é o último admin
            if (usuario.Permissao == PermissaoUsuario.Administrador)
            {
                 var totalAdmins = await _context.Usuarios
                     .CountAsync(u => u.Permissao == PermissaoUsuario.Administrador);
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
```

**Endpoints:**
- `POST /api/Usuarios` - Criar novo usuário (público)
- `GET /api/Usuarios` - Listar todos os usuários (Admin/Suporte)
- `GET /api/Usuarios/{id}` - Buscar usuário por ID (Admin/Suporte)
- `PUT /api/Usuarios/meu-perfil` - Atualizar próprio perfil (qualquer usuário)
- `PUT /api/Usuarios/{id}` - Atualizar qualquer usuário (Admin)
- `DELETE /api/Usuarios/{id}` - Excluir usuário (Admin)

---

## 🎫 3. CONTROLLER DE CHAMADOS (ChamadosController.cs)

### Responsabilidade: CRUD completo de chamados/tickets

```csharp
using ApiParaBD.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiParaBD.Controllers
{
    [Authorize] // Protege TODOS os endpoints nesta classe
    [ApiController]
    [Route("api/[controller]")]
    public class ChamadosController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public ChamadosController(ApplicationDbContext context)
        {
            _context = context;
        }

        // --- ENDPOINT PARA BUSCAR TODOS OS CHAMADOS ---
        [HttpGet]
        public async Task<IActionResult> GetChamados()
        {
            var chamados = await _context.Chamados
                .Include(c => c.Solicitante) // Inclui dados do usuário
                .Include(c => c.TecnicoResponsavel) // Inclui dados do técnico
                .ToListAsync();
            
            return Ok(chamados);
        }
        
        // --- ENDPOINT PARA BUSCAR UM CHAMADO POR ID ---
        [HttpGet("{id}")]
        public async Task<IActionResult> GetChamado(int id)
        {
            var chamado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            if (chamado == null)
            {
                return NotFound();
            }

            return Ok(chamado);
        }

        // --- ENDPOINT PARA CRIAR UM NOVO CHAMADO ---
        [HttpPost]
        public async Task<IActionResult> CriarChamado([FromBody] CriarChamadoDto chamadoDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var solicitante = await _context.Usuarios.FindAsync(chamadoDto.SolicitanteId);
            if (solicitante == null)
            {
                return BadRequest(new { message = "O usuário solicitante não foi encontrado." });
            }

            var novoChamado = new Chamado
            {
                Titulo = chamadoDto.Titulo,
                Descricao = chamadoDto.Descricao,
                Tipo = chamadoDto.Tipo,
                SolicitanteId = chamadoDto.SolicitanteId,
                DataAbertura = DateTime.UtcNow,
                Status = StatusChamado.Aberto,
                Prioridade = chamadoDto.Prioridade ?? PrioridadeChamado.Baixa 
            };

            _context.Chamados.Add(novoChamado);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetChamado), new { id = novoChamado.Id }, novoChamado);
        }

        // --- ENDPOINT PARA ATUALIZAR UM CHAMADO ---
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarChamado(int id, [FromBody] AtualizarChamadoDto atualizacaoDto)
        {
            var chamado = await _context.Chamados.FindAsync(id);
            if (chamado == null)
            {
                return NotFound(new { message = "Chamado não encontrado." });
            }

            // Atualiza campos dinamicamente se eles foram fornecidos no JSON
            if (atualizacaoDto.Status.HasValue)
            {
                chamado.Status = (StatusChamado)atualizacaoDto.Status.Value;
            }

            if (atualizacaoDto.TecnicoResponsavelId.HasValue)
            {
                var tecnico = await _context.Usuarios.FindAsync(atualizacaoDto.TecnicoResponsavelId.Value);
                if (tecnico == null)
                {
                    return BadRequest(new { message = "Técnico responsável não encontrado." });
                }
                chamado.TecnicoResponsavelId = atualizacaoDto.TecnicoResponsavelId.Value;
            }

            if (atualizacaoDto.DataFechamento.HasValue)
            {
                chamado.DataFechamento = atualizacaoDto.DataFechamento.Value;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Titulo))
            {
                chamado.Titulo = atualizacaoDto.Titulo;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Descricao))
            {
                chamado.Descricao = atualizacaoDto.Descricao;
            }

            if (atualizacaoDto.Prioridade.HasValue)
            {
                chamado.Prioridade = (PrioridadeChamado)atualizacaoDto.Prioridade.Value;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Solucao))
            {
                chamado.Solucao = atualizacaoDto.Solucao;
            }

            await _context.SaveChangesAsync();

            // Retornar o chamado atualizado com os dados relacionados
            var chamadoAtualizado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            return Ok(chamadoAtualizado);
        }
    }
}
```

**Endpoints:**
- `GET /api/Chamados` - Listar todos os chamados
- `GET /api/Chamados/{id}` - Buscar chamado por ID
- `POST /api/Chamados` - Criar novo chamado
- `PUT /api/Chamados/{id}` - Atualizar chamado existente

---

## 🏗️ 4. CONTEXTO DO BANCO DE DADOS (ApplicationDbContext.cs)

### Responsabilidade: Configurar Entity Framework e mapear entidades

```csharp
using Microsoft.EntityFrameworkCore;

namespace ApiParaBD 
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Usuario> Usuarios { get; set; }
        public DbSet<Chamado> Chamados { get; set; }
        public DbSet<HistoricoChamado> Historicos { get; set; }
    }
}
```

---

## 📦 5. MODELOS DE DADOS (Entidades)

### 5.1. Usuario.cs

```csharp
namespace ApiParaBD
{
    public class Usuario
    {
        public int Id { get; set; }
        public required string Nome { get; set; }
        public required string Email { get; set; }
        public required string SenhaHash { get; set; } // Nunca a senha real!
        public string? Telefone { get; set; }
        public required string Cargo { get; set; }
        public PermissaoUsuario Permissao { get; set; }
    }

    public enum PermissaoUsuario
    {
        Colaborador = 1,
        SuporteTecnico = 2,
        Administrador = 3
    }
}
```

### 5.2. Chamado.cs

```csharp
using System.ComponentModel.DataAnnotations.Schema;

namespace ApiParaBD
{
    public class Chamado
    {
        public int Id { get; set; }
        public required string Titulo { get; set; }
        public required string Descricao { get; set; }
        public DateTime DataAbertura { get; set; }
        public DateTime? DataFechamento { get; set; }
        public string? Solucao { get; set; } // Texto da solução fornecida pelo técnico

        // Relacionamentos (Chaves Estrangeiras)
        public int SolicitanteId { get; set; }
        [ForeignKey("SolicitanteId")]
        public virtual Usuario Solicitante { get; set; } = null!;

        public int? TecnicoResponsavelId { get; set; }
        [ForeignKey("TecnicoResponsavelId")]
        public virtual Usuario? TecnicoResponsavel { get; set; }

        // Categorização
        public PrioridadeChamado Prioridade { get; set; }
        public StatusChamado Status { get; set; }
        public required string Tipo { get; set; }
    }

    public enum PrioridadeChamado
    {
        Baixa = 1,
        Media = 2,
        Alta = 3,
    }

    public enum StatusChamado
    {
        Aberto = 1,
        EmAtendimento = 2,
        AguardandoUsuario = 3,
        Resolvido = 4,
        Fechado = 5
    }
}
```

### 5.3. HistoricoChamado.cs

```csharp
namespace ApiParaBD
{
    public class HistoricoChamado
    {
        public int Id { get; set; }
        public required string Mensagem { get; set; }
        public DateTime DataOcorrencia { get; set; }
        public bool EhMensagemDeIA { get; set; } = false; // Para identificar sugestões da IA

        // Relacionamentos
        public int ChamadoId { get; set; }
        public virtual Chamado Chamado { get; set; } = null!;

        // Quem enviou a mensagem? (Pode ser nulo se for uma mensagem do sistema/IA)
        public int? UsuarioId { get; set; }
        public virtual Usuario? Usuario { get; set; }
    }
}
```

---

## 📝 6. DATA TRANSFER OBJECTS (DTOs)

### 6.1. CriarUsuarioDto.cs

```csharp
namespace ApiParaBD.DTOs 
{
    public class CriarUsuarioDto
    {
        public required string Nome { get; set; }
        public required string Email { get; set; }
        public required string Senha { get; set; }
        public string? Telefone { get; set; }
        public required string Cargo { get; set; }
        public PermissaoUsuario Permissao { get; set; }
    }
}
```

### 6.2. AtualizarUsuarioDto.cs

```csharp
namespace ApiParaBD.DTOs
{
    public class AtualizarUsuarioDto
    {
        public string? Nome { get; set; }
        public string? Email { get; set; }
        public string? Telefone { get; set; }
        public string? Cargo { get; set; }
    }
}
```

### 6.3. CriarChamadoDto.cs

```csharp
namespace ApiParaBD.DTOs
{
    public class CriarChamadoDto
    {
        public required string Titulo { get; set; }
        public required string Descricao { get; set; }
        public required string Tipo { get; set; } // Ex: "Hardware", "Software", "Rede"
        public int SolicitanteId { get; set; }
        public PrioridadeChamado? Prioridade { get; set; }
    }
}
```

### 6.4. AtualizarChamadoDto.cs

```csharp
using System;

namespace ApiParaBD.DTOs
{
    public class AtualizarChamadoDto
    {
        public int? Status { get; set; }
        public int? TecnicoResponsavelId { get; set; }
        public DateTime? DataFechamento { get; set; }
        public string? Titulo { get; set; }
        public string? Descricao { get; set; }
        public string? Solucao { get; set; }
        public int? Prioridade { get; set; }
    }
}
```

### 6.5. LoginDto.cs

```csharp
namespace ApiParaBD.DTOs
{
    public class LoginDto
    {
        public required string Email { get; set; }
        public required string Senha { get; set; }
    }
}
```

### 6.6. LoginResponseDto.cs

```csharp
public class LoginResponseDto
{
    public required string Token { get; set; }
}
```

---

## ⚙️ 7. CONFIGURAÇÃO DA APLICAÇÃO (Program.cs)

### Responsabilidade: Configurar serviços, autenticação JWT e pipeline HTTP

```csharp
using ApiParaBD;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// --- 1. Serviços ---
builder.Services.AddControllers();

// DbContext
var connectionString = builder.Configuration.GetConnectionString("AzureSql");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// JWT Authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(
                builder.Configuration["Jwt:Key"] ?? string.Empty)),
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Jwt:Audience"],
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });
builder.Services.AddAuthorization();

// Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "API Suporte Técnico", Version = "v1" });
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        In = ParameterLocation.Header,
        Description = "Insira 'Bearer {seu_token}'",
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
    options.AddSecurityRequirement(new OpenApiSecurityRequirement {
        {
            new OpenApiSecurityScheme {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" },
                Scheme = "oauth2", Name = "Bearer", In = ParameterLocation.Header
            },
            Array.Empty<string>()
        }
    });
});

var app = builder.Build();

// --- 2. Pipeline HTTP ---
app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();
app.UseAuthentication(); // Ordem correta
app.UseAuthorization();  // Ordem correta
app.MapControllers();
app.MapGet("/", () => Results.Redirect("/swagger"));

app.Run();
```

---

## 🔍 8. HEALTH CHECK (HealthCheckController.cs)

### Responsabilidade: Verificar status da API

```csharp
using Microsoft.AspNetCore.Mvc;

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class HealthCheckController : ControllerBase
    {
        [HttpGet]
        public IActionResult Get()
        {
            return Ok(new { Status = "API está online e funcionando!", Timestamp = DateTime.UtcNow });
        }
    }
}
```

**Endpoint:**
- `GET /api/HealthCheck` - Verifica se a API está online

---

## 📊 Resumo das Operações CRUD

### Usuários
| Operação | Método | Endpoint | Autenticação |
|----------|--------|----------|--------------|
| Criar | POST | `/api/Usuarios` | Público |
| Listar | GET | `/api/Usuarios` | Admin/Suporte |
| Buscar | GET | `/api/Usuarios/{id}` | Admin/Suporte |
| Atualizar Perfil | PUT | `/api/Usuarios/meu-perfil` | Qualquer usuário |
| Atualizar | PUT | `/api/Usuarios/{id}` | Admin |
| Excluir | DELETE | `/api/Usuarios/{id}` | Admin |

### Chamados
| Operação | Método | Endpoint | Autenticação |
|----------|--------|----------|--------------|
| Listar | GET | `/api/Chamados` | Autenticado |
| Buscar | GET | `/api/Chamados/{id}` | Autenticado |
| Criar | POST | `/api/Chamados` | Autenticado |
| Atualizar | PUT | `/api/Chamados/{id}` | Autenticado |

### Autenticação
| Operação | Método | Endpoint | Autenticação |
|----------|--------|----------|--------------|
| Login | POST | `/api/Auth/login` | Público |

---

## 🔒 Segurança

- ✅ **Autenticação JWT** - Tokens expiram em 8 horas
- ✅ **Autorização por Role** - Permissões hierárquicas (Colaborador, SuporteTecnico, Administrador)
- ✅ **Hash de Senhas** - BCrypt para armazenamento seguro
- ✅ **Validação de Entrada** - ModelState validation
- ✅ **Proteção contra Enumeração** - Mensagens de erro genéricas

---

## 📦 Dependências Principais

- **.NET 9.0** - Framework
- **Entity Framework Core 9.0.9** - ORM
- **Microsoft.AspNetCore.Authentication.JwtBearer** - Autenticação JWT
- **BCrypt.Net** - Hash de senhas
- **Swagger/OpenAPI** - Documentação da API

---

**Documento gerado em:** `DateTime.Now`  
**Versão da API:** 1.0  
**Framework:** .NET 9.0

