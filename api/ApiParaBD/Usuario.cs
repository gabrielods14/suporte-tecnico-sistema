namespace ApiParaBD
{
    public class Usuario
    {
        public int Id { get; set; }
        public required string Nome { get; set; }
        public required string Email { get; set; }
        public required string SenhaHash { get; set; } // Nunca a senha real!
        public string? Telefone { get; set; }
        public required string Cargo { get; set; }
        public PermissaoUsuario Permissao { get; set; } // Usando o Enum
        public bool PrimeiroAcesso { get; set; } = true; // Novo campo para primeiro acesso

    }

    public enum PermissaoUsuario
    {
        Colaborador = 1,
        SuporteTecnico = 2,
        Administrador = 3
    }
}