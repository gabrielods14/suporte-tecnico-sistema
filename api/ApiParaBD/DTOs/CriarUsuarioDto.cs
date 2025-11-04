// DTOs/CriarUsuarioDto.cs
namespace ApiParaBD.DTOs 
{
    // Esta classe define apenas os dados necessários para criar um novo usuário.
    public class CriarUsuarioDto
    {
        public required string Nome { get; set; }
        public required string Email { get; set; }
        public required string Senha { get; set; } // A senha em texto puro, que será convertida em hash.
        public string? Telefone { get; set; }
        public required string Cargo { get; set; }
        public PermissaoUsuario Permissao { get; set; }
    }
}
