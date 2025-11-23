using ApiParaBD.DTOs; // Necessário para os DTOs
using Microsoft.AspNetCore.Authorization; // Necessário para [Authorize]
using Microsoft.AspNetCore.Mvc; // Necessário para ControllerBase
using Microsoft.EntityFrameworkCore; // Necessário para Include e operações assíncronas

namespace ApiParaBD.Controllers
{
    [Authorize] // Protege todos os endpoints: só usuários logados acessam
    [ApiController]
    [Route("api/[controller]")]
    public class ChamadosController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public ChamadosController(ApplicationDbContext context)
        {
            _context = context;
        }

        // --- GET: Listar todos os chamados ---
        [HttpGet]
        public async Task<IActionResult> GetChamados()
        {
            var chamados = await _context.Chamados
                .Include(c => c.Solicitante) // Carrega dados do usuário
                .Include(c => c.TecnicoResponsavel) // Carrega dados do técnico
                .ToListAsync();

            return Ok(chamados);
        }

        // --- GET: Buscar um chamado específico ---
        [HttpGet("{id}")]
        public async Task<IActionResult> GetChamado(int id)
        {
            var chamado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            if (chamado == null)
            {
                return NotFound(new { message = "Chamado não encontrado." });
            }

            return Ok(chamado);
        }

        // --- POST: Criar um novo chamado ---
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
                
                // Definições Automáticas Iniciais
                DataAbertura = DateTime.UtcNow,
                Status = StatusChamado.Aberto,
                Prioridade = chamadoDto.Prioridade ?? PrioridadeChamado.Baixa
            };

            _context.Chamados.Add(novoChamado);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetChamado), new { id = novoChamado.Id }, novoChamado);
        }

        // --- PUT: Atualizar Chamado (Status, Técnico, Solução) ---
        [HttpPut("{id}")]
        public async Task<IActionResult> AtualizarChamado(int id, [FromBody] AtualizarChamadoDto atualizacaoDto)
        {
            var chamado = await _context.Chamados.FindAsync(id);
            if (chamado == null)
            {
                return NotFound(new { message = "Chamado não encontrado." });
            }

            // 1. Lógica para Atribuição de Técnico
            if (atualizacaoDto.TecnicoResponsavelId.HasValue)
            {
                var tecnico = await _context.Usuarios.FindAsync(atualizacaoDto.TecnicoResponsavelId.Value);
                if (tecnico == null)
                {
                    return BadRequest(new { message = "Técnico responsável não encontrado." });
                }
                
                chamado.TecnicoResponsavelId = atualizacaoDto.TecnicoResponsavelId.Value;

                // AUTOMATIZAÇÃO: Se estava "Aberto" e ganhou um técnico -> "Em Atendimento"
                if (chamado.Status == StatusChamado.Aberto)
                {
                    chamado.Status = StatusChamado.EmAtendimento;
                }
            }

            // 2. Lógica para Solução e Fechamento
            if (!string.IsNullOrEmpty(atualizacaoDto.Solucao))
            {
                chamado.Solucao = atualizacaoDto.Solucao;
                
                // AUTOMATIZAÇÃO: Se tem solução -> Fecha o chamado automaticamente
                chamado.Status = StatusChamado.Fechado;
                chamado.DataFechamento = DateTime.UtcNow;
            }

            // 3. Atualizações Manuais (caso o usuário queira mudar explicitamente)
            if (atualizacaoDto.Status.HasValue)
            {
                chamado.Status = (StatusChamado)atualizacaoDto.Status.Value;
            }

            if (atualizacaoDto.DataFechamento.HasValue)
            {
                chamado.DataFechamento = atualizacaoDto.DataFechamento.Value;
            }

            if (!string.IsNullOrEmpty(atualizacaoDto.Titulo)) chamado.Titulo = atualizacaoDto.Titulo;
            if (!string.IsNullOrEmpty(atualizacaoDto.Descricao)) chamado.Descricao = atualizacaoDto.Descricao;
            if (atualizacaoDto.Prioridade.HasValue) chamado.Prioridade = (PrioridadeChamado)atualizacaoDto.Prioridade.Value;

            // Salvar tudo no banco
            await _context.SaveChangesAsync();

            // Retornar o objeto atualizado com os dados relacionados (para a tela atualizar na hora)
            var chamadoAtualizado = await _context.Chamados
                .Include(c => c.Solicitante)
                .Include(c => c.TecnicoResponsavel)
                .FirstOrDefaultAsync(c => c.Id == id);

            return Ok(chamadoAtualizado);
        }
    }
}
