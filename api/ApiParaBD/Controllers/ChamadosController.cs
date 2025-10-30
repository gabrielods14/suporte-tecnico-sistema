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

        // --- ENDPOINT PARA ATUALIZAR UM CHAMADO ---
        // PUT /api/Chamados/{id}
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarChamado(int id, [FromBody] AtualizarChamadoDto atualizacaoDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            // Buscar o chamado existente
            var chamado = await _context.Chamados.FindAsync(id);
            if (chamado == null)
            {
                return NotFound(new { message = "Chamado não encontrado." });
            }

            // Atualizar apenas os campos fornecidos
            if (atualizacaoDto.Status.HasValue)
            {
                chamado.Status = (StatusChamado)atualizacaoDto.Status.Value;
            }

            if (atualizacaoDto.TecnicoResponsavelId.HasValue)
            {
                // Verificar se o técnico existe
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

            if (!string.IsNullOrEmpty(atualizacaoDto.Solucao))
            {
                chamado.Solucao = atualizacaoDto.Solucao;
            }

            if (atualizacaoDto.Prioridade.HasValue)
            {
                chamado.Prioridade = (PrioridadeChamado)atualizacaoDto.Prioridade.Value;
            }

            // Salvar as alterações
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
