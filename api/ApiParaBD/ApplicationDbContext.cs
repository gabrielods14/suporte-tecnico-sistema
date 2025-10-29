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
        
        // Adicionar configurações de modelo aqui se necessário (ex: chaves compostas)
        // protected override void OnModelCreating(ModelBuilder modelBuilder)
        // {
        //     base.OnModelCreating(modelBuilder);
        //     // Configurações...
        // }
    }
}
