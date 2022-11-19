namespace lan_management_api.Services;

public interface IAccountService
{
    void Register(RegisterRequest model, string origin);
    IEnumerable<AccountResponse> GetAll();
    AccountResponse Create(CreateRequest model);
    AccountResponse GetById(int id);
    void Delete(int id);
    AccountResponse Update(int id, UpdateRequest model);
}