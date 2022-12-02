namespace lan_management_api.Controllers;

public abstract class BaseController : ControllerBase
{
    public Account Account => (Account) HttpContext.Items["Account"];
}