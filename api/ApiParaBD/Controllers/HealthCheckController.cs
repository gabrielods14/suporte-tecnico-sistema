using Microsoft.AspNetCore.Mvc;

namespace ApiParaBD.Controllers
{
    [ApiController]
    [Route("api/[controller]")] // Rota será /api/HealthCheck
    public class HealthCheckController : ControllerBase
    {
        [HttpGet] // Este método responderá a requisições GET
        public IActionResult Get()
        {
            return Ok(new { Status = "API está online e funcionando!", Timestamp = DateTime.UtcNow });
        }
    }
}