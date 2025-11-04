// DTOs/AtualizarUsuarioDto.cs

// Esta classe define os dados que podem ser atualizados no perfil do usuário.
public class AtualizarUsuarioDto
{
    public string? Nome { get; set; }
    public string? Email { get; set; }
    public string? Telefone { get; set; }
    public string? Cargo { get; set; }
    // Nota: Senha e Permissao não estão incluídos por segurança
    // A atualização de senha deve ser feita em um endpoint separado
    // A permissão deve ser alterada apenas por administradores
}

