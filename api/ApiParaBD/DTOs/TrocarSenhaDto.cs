// DTO usado para receber os dados necessários para trocar a senha de um usuário
namespace ApiParaBD.DTOs
{
    public class TrocarSenhaDto
    {
        public required string SenhaAtual { get; set; }
        public required string NovaSenha { get; set; }
    }
}