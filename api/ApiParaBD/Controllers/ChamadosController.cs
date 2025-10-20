using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")] // Rota será /api/Chamados
    public class ChamadosController : ControllerBase
    {
        private readonly AppContext _context;

        public ChamadosController(AppContext context)
        {
            _context = context;
        }

        // --- ENDPOINT PARA BUSCAR TODOS OS CHAMADOS ---
        // GET /api/Chamados
        [HttpGet]
        public async Task<IActionResult> GetChamados()
        {
            // Usamos .Include() para carregar os dados do usuário solicitante junto com o chamado.
            // Isso evita o problema de "lazy loading" e torna a resposta mais completa.
            var chamados = await _context.Chamados
                .Include(c => c.Solicitante) // Inclui os dados do usuário que abriu o chamado
                .Include(c => c.TecnicoResponsavel) // Inclui os dados do técnico, se houver
                .ToListAsync();
            
            return Ok(chamados);
        }
        
        // --- ENDPOINT PARA BUSCAR UM CHAMADO POR ID ---
        // GET /api/Chamados/5
        [HttpGet("{id}")]
        public async Task<IActionResult> GetChamado(int id)
        {
            var chamado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            if (chamado == null)
            {
                return NotFound(); // Retorna 404 se o chamado não for encontrado
            }

            return Ok(chamado);
        }

        // --- ENDPOINT PARA CRIAR UM NOVO CHAMADO ---
        // POST /api/Chamados
        [HttpPost]
        public async Task<IActionResult> CriarChamado([FromBody] CriarChamadoDto chamadoDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            // Verifica se o usuário que está abrindo o chamado realmente existe.
            var solicitante = await _context.Usuarios.FindAsync(chamadoDto.SolicitanteId);
            if (solicitante == null)
            {
                // Retorna um erro claro se o ID do solicitante for inválido.
                return BadRequest(new { message = "O usuário solicitante não foi encontrado." });
            }

            var novoChamado = new Chamado
            {
                Titulo = chamadoDto.Titulo,
                Descricao = chamadoDto.Descricao,
                Tipo = chamadoDto.Tipo,
                SolicitanteId = chamadoDto.SolicitanteId,

                // A API define os valores iniciais padrão, garantindo consistência.
                DataAbertura = DateTime.UtcNow,
                Status = StatusChamado.Aberto,
                // Se o cliente não enviar uma prioridade, definimos como "Baixa".
                Prioridade = chamadoDto.Prioridade ?? PrioridadeChamado.Baixa 
            };

            _context.Chamados.Add(novoChamado);
            await _context.SaveChangesAsync();

            // Retorna 201 Created com a localização do novo chamado e o objeto criado.
            return CreatedAtAction(nameof(GetChamado), new { id = novoChamado.Id }, novoChamado);
        }
    }
}
