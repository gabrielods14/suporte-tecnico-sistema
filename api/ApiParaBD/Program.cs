// --- Imports necessários ---
using ApiParaBD;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;
using System.IO;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

// --- 1. Serviços ---
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        // Ignorar referências circulares na serialização JSON
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
        options.JsonSerializerOptions.WriteIndented = true;
    });

// DbContext (com nome corrigido)
var connectionString = builder.Configuration.GetConnectionString("AzureSql");
builder.Services.AddDbContext<ApplicationDbContext>(options => // <-- NOME CORRIGIDO
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(30),
            errorNumbersToAdd: null);
    }));

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
    
    // Configuração de segurança JWT
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
    
    // Ignorar referências circulares e propriedades de navegação do EF Core
    options.CustomSchemaIds(type => type.FullName?.Replace("+", "."));
    options.IgnoreObsoleteActions();
    options.IgnoreObsoleteProperties();
    
    // Configurar para não depender do DbContext na geração do schema
    options.UseAllOfToExtendReferenceSchemas();
    options.UseOneOfForPolymorphism();
    options.UseAllOfForInheritance();
    
    // Incluir comentários XML se existirem
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        options.IncludeXmlComments(xmlPath);
    }
});

var app = builder.Build();

// --- 2. Pipeline HTTP ---
// Swagger - sempre disponível, mesmo em produção (pode ser restrito depois se necessário)
app.UseSwagger(c =>
{
    c.RouteTemplate = "swagger/{documentName}/swagger.json";
});

app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "API Suporte Técnico v1");
    c.RoutePrefix = "swagger";
    c.DisplayRequestDuration();
    c.EnableTryItOutByDefault();
});

// Middleware de tratamento de erros
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsync("{\"error\":\"Ocorreu um erro interno no servidor.\"}");
    });
});
app.UseStatusCodePages();

app.UseHttpsRedirection();
app.UseAuthentication(); // <-- Ordem correta
app.UseAuthorization();  // <-- Ordem correta
app.MapControllers();
app.MapGet("/", () => Results.Redirect("/swagger"));

// Endpoint de erro para debug
app.MapGet("/error", () => Results.Problem("Ocorreu um erro ao processar a requisição."));

app.Run();
