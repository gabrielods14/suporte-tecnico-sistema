using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiParaBD.Migrations
{
    /// <inheritdoc />
    public partial class AdicionarColunaSolucao : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Solucao",
                table: "Chamados",
                type: "nvarchar(max)",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Solucao",
                table: "Chamados");
        }
    }
}
