// DTO usado para receber os dados de login do cliente
namespace ApiParaBD.DTOs
{
    // Define os dados que um cliente deve enviar para fazer login
    public class LoginDto
    {
        public required string Email { get; set; }
        public required string Senha { get; set; }
    }
}
