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

        // --- A MÁGICA ACONTECE AQUI (DATA SEEDING) ---
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            
            modelBuilder.Entity<Usuario>().HasData(
                new Usuario
                {
                    Id = 1,
                    Nome = "Administrador Sistema",
                    Email = "admin@helpwave.com",
                    SenhaHash = "$2a$11$8wYso8QevHE6MfV4JQoF5O2vlvvQyPnBVUL7ywtQ8p1gmSaPtK8nK", 
                    Telefone = "12999999999",
                    Cargo = "Gestor de TI",
                    Permissao = PermissaoUsuario.Administrador
                },
                new Usuario
                {
                    Id = 2,
                    Nome = "Técnico Padrão",
                    Email = "tecnico@helpwave.com",
                    SenhaHash = "$2a$11$8wYso8QevHE6MfV4JQoF5O2vlvvQyPnBVUL7ywtQ8p1gmSaPtK8nK",
                    Telefone = "12888888888",
                    Cargo = "Suporte N1",
                    Permissao = PermissaoUsuario.SuporteTecnico
                }
            );
        }
    }
}