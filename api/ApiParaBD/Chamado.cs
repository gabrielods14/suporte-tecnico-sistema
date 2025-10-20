using System.ComponentModel.DataAnnotations.Schema;

public class Chamado
{
    public int Id { get; set; } // ID de identificação
    public required string Titulo { get; set; }
    public required string Descricao { get; set; }
    public DateTime DataAbertura { get; set; }
    public DateTime? DataFechamento { get; set; }

    // --- Relacionamentos (Chaves Estrangeiras) ---

    // Quem abriu o chamado?
    public int SolicitanteId { get; set; }
    [ForeignKey("SolicitanteId")]
    public virtual Usuario Solicitante { get; set; } = null!;

    // Quem está atendendo o chamado? (Pode ser nulo no início)
    public int? TecnicoResponsavelId { get; set; }
    [ForeignKey("TecnicoResponsavelId")]
    public virtual Usuario? TecnicoResponsavel { get; set; }

    // --- Categorização ---
    public PrioridadeChamado Prioridade { get; set; }
    public StatusChamado Status { get; set; }
    public required string Tipo { get; set; } // Ex: "Hardware", "Software", "Rede"
}

public enum PrioridadeChamado
{
    Baixa = 1,
    Media = 2,
    Alta = 3
}

public enum StatusChamado
{
    Aberto = 1,
    EmAtendimento = 2,
    AguardandoUsuario = 3,
    Resolvido = 4,
    Fechado = 5
}