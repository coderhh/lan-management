namespace lan_management_api.Services;

public interface IAccountService
{
    void Register(RegisterRequest model, string origin);
    Task<IEnumerable<AccountResponse>> GetAll();
    Task<AccountResponse> Create(CreateRequest model);
    Task<AccountResponse> GetById(int id);
    Task<bool> Delete(int id);
    Task<AccountResponse> Update(int id, UpdateRequest model);
    Task<bool> DeleteAll();
}