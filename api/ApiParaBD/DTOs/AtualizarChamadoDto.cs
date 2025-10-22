// DTOs/AtualizarChamadoDto.cs

// Define os dados que um cliente pode enviar para atualizar um chamado existente
public class AtualizarChamadoDto
{
    public int? Status { get; set; } // Novo status do chamado
    public int? TecnicoResponsavelId { get; set; } // ID do técnico responsável
    public DateTime? DataFechamento { get; set; } // Data de fechamento (se aplicável)
    public string? Titulo { get; set; } // Título atualizado
    public string? Descricao { get; set; } // Descrição atualizada
    public int? Prioridade { get; set; } // Nova prioridade
}


