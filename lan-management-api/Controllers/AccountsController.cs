using Org.BouncyCastle.Tls;

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
    public ActionResult<IEnumerable<AccountResponse>> GetAll()
    {
        var accounts = _accountService.GetAll();
        return Ok(accounts);
    }

    [AllowAnonymous]
    [HttpPost]
    public ActionResult<AccountResponse> Create(CreateRequest model)
    {
        var account = _accountService.Create(model);
        return Ok(account);
    }

    [AllowAnonymous]
    [HttpGet("{id:int}")]
    public ActionResult<AccountResponse> GetById(int id)
    {
        var account = _accountService.GetById(id);
        return Ok(account);
    }
    [AllowAnonymous]
    [HttpDelete("{id:int}")]
    public IActionResult Delete(int id)
    {
        _accountService.Delete(id);
        return Ok(new {message = "Account deleted successfully"});
    }
    [AllowAnonymous]
    [HttpPut("{id:int}")]
    public ActionResult<AccountResponse> Update(int id, UpdateRequest model)
    {
        var account = _accountService.Update(id, model);
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