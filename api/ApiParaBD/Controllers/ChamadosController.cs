using ApiParaBD.DTOs; // Importa seus DTOs
using Microsoft.AspNetCore.Authorization; // Importa a segurança
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiParaBD.Controllers
{
    [Authorize] // <-- ISSO PROTEGE TODOS OS ENDPOINTS NESTA CLASSE
    [ApiController]
    [Route("api/[controller]")]
    public class ChamadosController : ControllerBase
    {
        // Usando o nome do DbContext corrigido
        private readonly ApplicationDbContext _context;

        public ChamadosController(ApplicationDbContext context)
        {
            _context = context;
        }

        // --- ENDPOINT PARA BUSCAR TODOS OS CHAMADOS ---
        [HttpGet]
        public async Task<IActionResult> GetChamados()
        {
            var chamados = await _context.Chamados
                .Include(c => c.Solicitante) // Inclui dados do usuário
                .Include(c => c.TecnicoResponsavel) // Inclui dados do técnico
                .ToListAsync();

            return Ok(chamados);
        }

        // --- ENDPOINT PARA BUSCAR UM CHAMADO POR ID ---
        [HttpGet("{id}")]
        public async Task<IActionResult> GetChamado(int id)
        {
            var chamado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            if (chamado == null)
            {
                return NotFound();
            }

            return Ok(chamado);
        }

        // --- ENDPOINT PARA CRIAR UM NOVO CHAMADO ---
        [HttpPost]
        public async Task<IActionResult> CriarChamado([FromBody] CriarChamadoDto chamadoDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var solicitante = await _context.Usuarios.FindAsync(chamadoDto.SolicitanteId);
            if (solicitante == null)
            {
                return BadRequest(new { message = "O usuário solicitante não foi encontrado." });
            }

            var novoChamado = new Chamado
            {
                Titulo = chamadoDto.Titulo,
                Descricao = chamadoDto.Descricao,
                Tipo = chamadoDto.Tipo,
                SolicitanteId = chamadoDto.SolicitanteId,
                DataAbertura = DateTime.UtcNow,
                Status = StatusChamado.Aberto,
                Prioridade = chamadoDto.Prioridade ?? PrioridadeChamado.Baixa
            };

            _context.Chamados.Add(novoChamado);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetChamado), new { id = novoChamado.Id }, novoChamado);
        }

        // --- ENDPOINT PARA ATUALIZAR UM CHAMADO ---
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarChamado(int id, [FromBody] AtualizarChamadoDto atualizacaoDto)
        {
            var chamado = await _context.Chamados.FindAsync(id);
            if (chamado == null)
            {
                return NotFound(new { message = "Chamado não encontrado." });
            }

            // Atualiza campos dinamicamente se eles foram fornecidos no JSON
            if (atualizacaoDto.Status.HasValue)
            {
                chamado.Status = (StatusChamado)atualizacaoDto.Status.Value;
            }

            if (atualizacaoDto.TecnicoResponsavelId.HasValue)
            {
                var tecnico = await _context.Usuarios.FindAsync(atualizacaoDto.TecnicoResponsavelId.Value);
                if (tecnico == null)
                {
                    return BadRequest(new { message = "Técnico responsável não encontrado." });
                }
                chamado.TecnicoResponsavelId = atualizacaoDto.TecnicoResponsavelId.Value;
            }

            if (atualizacaoDto.DataFechamento.HasValue)
            {
                chamado.DataFechamento = atualizacaoDto.DataFechamento.Value;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Titulo))
            {
                chamado.Titulo = atualizacaoDto.Titulo;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Descricao))
            {
                chamado.Descricao = atualizacaoDto.Descricao;
            }

            if (atualizacaoDto.Prioridade.HasValue)
            {
                chamado.Prioridade = (PrioridadeChamado)atualizacaoDto.Prioridade.Value;
            }

            // --- LÓGICA DA SUA NOVA FUNCIONALIDADE ---
            if (!string.IsNullOrEmpty(atualizacaoDto.Solucao))
            {
                chamado.Solucao = atualizacaoDto.Solucao;
            }

            await _context.SaveChangesAsync();

            // Retornar o chamado atualizado com os dados relacionados
            var chamadoAtualizado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            return Ok(chamadoAtualizado);
        }
    }
}

