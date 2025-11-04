// DTOs/LoginResponseDto.cs
namespace ApiParaBD.DTOs
{
    // Define os dados que o servidor retorna ao cliente após um login bem-sucedido
    public class LoginResponseDto
    {
        public required string Token { get; set; }
    }
}
