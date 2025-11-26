// DTO usado para atualizar informações de um usuário pelo Admin
namespace ApiParaBD.DTOs
{
    public class AtualizarUsuarioAdminDto
    {
        public string? Nome { get; set; }
        public string? Email { get; set; }
        public string? Telefone { get; set; }
        public string? Cargo { get; set; }
        public PermissaoUsuario? Permissao { get; set; } // Admin pode mudar permissão

        // Se o Admin preencher isso, a senha será resetada. Se deixar null, mantém a atual.
        public string? NovaSenha { get; set; } 
    }
}