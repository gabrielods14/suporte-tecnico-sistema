namespace ApiParaBD
{
    public class HistoricoChamado
    {
        public int Id { get; set; }
        public required string Mensagem { get; set; }
        public DateTime DataOcorrencia { get; set; }
        public bool EhMensagemDeIA { get; set; } = false; // Para identificar sugestões da IA

        // --- Relacionamentos ---
        public int ChamadoId { get; set; }
        public virtual Chamado Chamado { get; set; } = null!;

        // Quem enviou a mensagem? (Pode ser nulo se for uma mensagem do sistema/IA)
        public int? UsuarioId { get; set; }
        public virtual Usuario? Usuario { get; set; }
    }
}