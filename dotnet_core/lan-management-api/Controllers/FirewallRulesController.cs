namespace lan_management_api.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class FirewallRulesController: BaseController
{
    private readonly ILogger<FirewallRulesController> _logger;
    public FirewallRulesController(ILogger<FirewallRulesController> logger)
    {
        _logger = logger;
    }

    [AllowAnonymous]
    [HttpGet]
    public async Task GetAll()
    {
        
    }
}