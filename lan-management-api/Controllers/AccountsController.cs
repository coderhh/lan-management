using lan_management_api.Models.Accounts;
using lan_management_api.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace lan_management_api.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class AccountsController : BaseController
{
    private readonly ILogger<AccountsController> _logger;
    private readonly IAccountService _accountService;

    public AccountsController(ILogger<AccountsController> logger, IAccountService accountService)
    {
        _logger = logger;
        _accountService = accountService;
    }

    [AllowAnonymous]
    [HttpPost("authenticate")]
    public ActionResult Authenticate()
    {
        return Ok();
    }

    [AllowAnonymous]
    [HttpPost("refresh-token")]
    public ActionResult RefreshToken()
    {
        return Ok();
    }

    [HttpPost("revoke-token")]
    public IActionResult RevokeToken()
    {
        return Ok();
    }

    [AllowAnonymous]
    [HttpPost("register")]
    public IActionResult Register(RegisterRequest model)
    {
        _accountService.Register(model, Request.Headers["origin"]);
        return Ok(new { message = "Please check your email for password reset instructions" });
    }
}