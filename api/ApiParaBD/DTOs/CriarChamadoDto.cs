// DTO usado para receber os dados de criação de um novo chamado
namespace ApiParaBD.DTOs
{
    // Define os dados que um cliente (web, desktop, etc.) precisa enviar para abrir um novo chamado.
    public class CriarChamadoDto
    {
        public required string Titulo { get; set; }
        public required string Descricao { get; set; }
        public required string Tipo { get; set; } // Ex: "Hardware", "Software", "Rede"

        // A API precisa saber QUEM está abrindo o chamado.
        public int SolicitanteId { get; set; }

        // A prioridade pode ser opcional na criação, e a API define um padrão.
        public PrioridadeChamado? Prioridade { get; set; }
    }
}