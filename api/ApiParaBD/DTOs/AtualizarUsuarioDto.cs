using ApiParaBD;

namespace ApiParaBD.DTOs
{
    public class AtualizarUsuarioDto
    {
        // Usamos 'string?' (nullable) para que o cliente possa enviar
        // apenas os campos que deseja atualizar.
        
        public string? Nome { get; set; }
        public string? Email { get; set; }
        public string? Telefone { get; set; }
        public string? Cargo { get; set; }
        public PermissaoUsuario? Permissao { get; set; } 
    }
}
