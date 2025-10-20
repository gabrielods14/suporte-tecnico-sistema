using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
var configuration = builder.Configuration; // Atalho para acessar as configurações

// --- SEÇÃO DE SERVIÇOS ---
builder.Services.AddControllers();

// Configuração do Entity Framework Core (seu código existente)
var connectionString = builder.Configuration.GetConnectionString("AzureSql");
builder.Services.AddDbContext<AppContext>(options => options.UseSqlServer(connectionString));

// --- NOVA CONFIGURAÇÃO DA AUTENTICAÇÃO JWT ---
// Aqui, "ensinamos" a API a usar o esquema de autenticação Bearer com JWTs.
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    // Aqui, definimos as regras para validar um token.
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true, // Validar quem emitiu o token
        ValidateAudience = true, // Validar para quem o token foi emitido
        ValidateLifetime = true, // Validar se o token não expirou
        ValidateIssuerSigningKey = true, // Validar a assinatura do token
        ValidIssuer = configuration["Jwt:Issuer"], // O emissor válido (do appsettings)
        ValidAudience = configuration["Jwt:Audience"], // O público válido (do appsettings)
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(configuration["Jwt:Key"]!)) // A chave secreta para validar a assinatura
    };
});

builder.Services.AddEndpointsApiExplorer();

// --- NOVA CONFIGURAÇÃO DO SWAGGER PARA USAR AUTENTICAÇÃO ---
// Adicionamos uma definição de segurança para que o Swagger saiba sobre o "Bearer token".
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "API de Suporte", Version = "v1" });
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Insira o token JWT com Bearer na frente (ex: 'Bearer {seu_token}')"
    });
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            new string[] {}
        }
    });
});


var app = builder.Build();

// --- SEÇÃO DE MIDDLEWARE ---
// A ordem dos middlewares é crucial para o funcionamento.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
else // Em produção, também queremos ver o Swagger UI
{
    app.UseSwagger();
    app.UseSwaggerUI();
}


app.UseHttpsRedirection();

// Adicionamos os middlewares de autenticação e autorização.
// A API primeiro verifica a autenticação (UseAuthentication)
// e depois verifica se o usuário autenticado tem permissão (UseAuthorization).
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapGet("/", () => Results.Redirect("/swagger")); // Seu redirecionamento

app.Run();