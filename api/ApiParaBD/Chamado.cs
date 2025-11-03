using System.ComponentModel.DataAnnotations.Schema;

namespace ApiParaBD // Verifique se este é o namespace raiz do projeto
{
    public class Chamado
    {
        public int Id { get; set; }
        public required string Titulo { get; set; }
        public required string Descricao { get; set; }
        public DateTime DataAbertura { get; set; }
        public DateTime? DataFechamento { get; set; }

        // --- SUA NOVA FUNCIONALIDADE ---
        public string? Solucao { get; set; } // Texto da solução fornecida pelo técnico

        // --- Relacionamentos (Chaves Estrangeiras) ---
        public int SolicitanteId { get; set; }
        [ForeignKey("SolicitanteId")]
        public virtual Usuario Solicitante { get; set; } = null!; // Garante que não é nulo

        public int? TecnicoResponsavelId { get; set; }
        [ForeignKey("TecnicoResponsavelId")]
        public virtual Usuario? TecnicoResponsavel { get; set; }

        // --- Categorização ---
        public PrioridadeChamado Prioridade { get; set; }
        public StatusChamado Status { get; set; }
        public required string Tipo { get; set; }
    }

    // Enums podem ficar aqui ou em arquivos separados
    public enum PrioridadeChamado
    {
        Baixa = 1,
        Media = 2,
        Alta = 3,
        Urgente = 4
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
