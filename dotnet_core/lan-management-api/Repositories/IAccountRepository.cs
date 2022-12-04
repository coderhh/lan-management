namespace lan_management_api.Repositories;

public interface IAccountRepository
{
    public Task<IEnumerable<Account>> GetAccountsByEmail(string email);
    public Task<Account> GetAccountByVerificationToken(string token);
    public Task<Account> GetAccountById(int id);
    public Task<IEnumerable<Account>> GetAllAccounts();
    public Task<Account> CreateAccount(Account account);
    public Task<bool> DeleteAllAccount();
    public Task<bool> DeleteAccountById(int id);
    public Task<bool> UpdateAccount(Account account);
}