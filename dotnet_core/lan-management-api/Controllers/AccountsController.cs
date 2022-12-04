namespace lan_management_api.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class AccountsController : BaseController
{
    private readonly IAccountService _accountService;
    private readonly ILogger<AccountsController> _logger;

    public AccountsController(ILogger<AccountsController> logger, IAccountService accountService)
    {
        _logger = logger;
        _accountService = accountService;
    }

    [AllowAnonymous]
    [HttpGet]
    public async Task<ActionResult<IEnumerable<AccountResponse>>> GetAll()
    {
        var accounts = await _accountService.GetAll();
        return Ok(accounts);
    }

    [AllowAnonymous]
    [HttpPost]
    public async Task<ActionResult<AccountResponse>> Create(CreateRequest model)
    {
        var account = await _accountService.Create(model);
        return Ok(account);
    }

    [AllowAnonymous]
    [HttpGet("{id:int}")]
    public async Task<ActionResult<AccountResponse>> GetById(int id)
    {
        var account = await _accountService.GetById(id);
        return Ok(account);
    }
    [AllowAnonymous]
    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
    {
        var result  = await _accountService.Delete(id);
        if (result)
        {
            return Ok(new {message = "Account deleted successfully"});
        }
        else
        {
            return BadRequest();
        }
    }
    
    [AllowAnonymous]
    [HttpDelete]
    public async Task<IActionResult> DeleteAll()
    {
        var res = await _accountService.DeleteAll();
        if (res)
        {
            return Ok(new {message = "All accounts deleted successfully"});
        }
        else
        {
            return BadRequest();
        }
    }
    [AllowAnonymous]
    [HttpPut("{id:int}")]
    public async Task<ActionResult<AccountResponse>> Update(int id, UpdateRequest model)
    {
        var account = await _accountService.Update(id, model);
        return Ok(account);
    }

    #region MyRegion

    // [AllowAnonymous]
    // [HttpPost("authenticate")]
    // public ActionResult Authenticate()
    // {
    //     return Ok();
    // }
    //
    // [AllowAnonymous]
    // [HttpPost("refresh-token")]
    // public ActionResult RefreshToken()
    // {
    //     return Ok();
    // }
    //
    // [HttpPost("revoke-token")]
    // public IActionResult RevokeToken()
    // {
    //     return Ok();
    // }
    //
    // [AllowAnonymous]
    // [HttpPost("register")]
    // public IActionResult Register(RegisterRequest model)
    // {
    //     _accountService.Register(model, Request.Headers["origin"]);
    //     return Ok(new {message = "Please check your email for password reset instructions"});
    // }

    #endregion
}