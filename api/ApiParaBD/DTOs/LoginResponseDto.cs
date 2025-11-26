// DTO usado para retornar o token JWT após login bem-sucedido
namespace ApiParaBD.DTOs
{
    public class LoginResponseDto
    {
        public required string Token { get; set; }
        public bool PrimeiroAcesso { get; set; } // // O frontend vai ler isso. Se for true, redireciona para tela de "Nova Senha"
    }
}