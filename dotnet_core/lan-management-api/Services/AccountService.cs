using System.Security.Cryptography;
using lan_management_api.Helpers;
using lan_management_api.Repositories;
using Microsoft.Extensions.Caching.Distributed;

namespace lan_management_api.Services;

public class AccountService : IAccountService
{
    private readonly DataContext _context;
    private readonly IEmailService _emailService;
    private readonly IMapper _mapper;
    private readonly IAccountRepository _accountRepository;
    private readonly IDistributedCache _cache;
    private readonly ILogger<AccountService> _logger;

    public AccountService(DataContext context,
        IEmailService emailService,
        IMapper mapper,
        IConfiguration configuration,
        IAccountRepository accountRepository, 
        IDistributedCache cache, 
        ILogger<AccountService> logger)
    {
        _context = context;
        _emailService = emailService;
        _mapper = mapper;
        _accountRepository = accountRepository;
        _cache = cache;
        _logger = logger;
    }
    public async void Register(RegisterRequest model, string origin)
    {
        if (_context.Accounts.Any(x => x.Email == model.Email))
        {
            //TODO send already registered error in email to prevent account enumeration
            SendAlreadyRegisteredEmail(model.Email, origin);
            return;
        }

        var account = _mapper.Map<Account>(model);
        var isFirstAccount = _context.Accounts.Count() == 0;
        account.Role = isFirstAccount ? Role.Admin : Role.User;
        account.Created = DateTime.UtcNow;
        account.VerificationToken = await GenerateVerificationToken();

        account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        _context.Accounts.Add(account);
        _context.SaveChanges();
    }
    public async Task<IEnumerable<AccountResponse>> GetAll()
    {
        IEnumerable<Account>? accounts;
        string recordKey = $"Accounts_{DateTime.Now:yyyyMMdd_hhmm}";
        accounts = await _cache.GetRecordAsync<IEnumerable<Account>>(recordKey);
        if (accounts is null)
        {
            _logger.LogInformation("cache missed");
            accounts = await _accountRepository.GetAllAccounts();
            await _cache.SetRecordAsync(recordKey, accounts);
        }
    
        return _mapper.Map<IList<AccountResponse>>(accounts);
    }
    public async Task<AccountResponse> Create(CreateRequest model)
    {
        #region Dapper Implementation
        var accounts = await _accountRepository.GetAccountsByEmail(model.Email);
        if (accounts.Any())
        {
            throw new AppException($"Email '{model.Email}' is already registered");
        }
        var account = _mapper.Map<Account>(model);
        account.Created = DateTime.UtcNow;
        account.Verified = DateTime.UtcNow;
        account.VerificationToken = await GenerateVerificationToken();
        account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        var result = await _accountRepository.CreateAccount(account);
        
        return _mapper.Map<AccountResponse>(result);

        #endregion
    }
    public async Task<AccountResponse> GetById(int id)
    {
        Account? account;
        string recordKey = $"Accounts_{id}_{DateTime.Now:yyyyMMdd_hhmm}";
        account = await _cache.GetRecordAsync<Account>(recordKey);
        if (account is null)
        {
            account = await _accountRepository.GetAccountById(id);
            if (account == null) throw new KeyNotFoundException("Account not found");
            _logger.LogInformation("cache missed");
            await _cache.SetRecordAsync(recordKey, account);
        }
        
        return _mapper.Map<AccountResponse>(account);
    }
    public async Task<bool> Delete(int id)
    {
        return await _accountRepository.DeleteAccountById(id);
    }
    public async Task<AccountResponse> Update(int id, UpdateRequest model)
    {
        var account = await GetAccount(id);
        var accountWithSameEmail = await _accountRepository.GetAccountsByEmail(model.Email);
        if (account.Email != model.Email && accountWithSameEmail.Any())
            throw new AppException($"Email '{model.Email}' is already registered");

        if (!string.IsNullOrEmpty(model.Password))
            account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        _mapper.Map(model, account);
        account.Updated = DateTime.UtcNow;
        await _accountRepository.UpdateAccount(account);

        return _mapper.Map<AccountResponse>(account);
    }
    public async Task<bool> DeleteAll()
    {
        var res = await _accountRepository.DeleteAllAccount();
        return res;
    }
    private async Task<Account> GetAccount(int id)
    {
        Account? account;
        string recordKey = $"Accounts_{id}_{DateTime.Now:yyyyMMdd_hhmm}";
        account = await _cache.GetRecordAsync<Account>(recordKey);
        if (account is null)
        {
            account = await _accountRepository.GetAccountById(id);
            if (account == null) throw new KeyNotFoundException("Account not found");
            _logger.LogInformation("cache missed");
            await _cache.SetRecordAsync(recordKey, account);
        }
       
        return account;
    }
    private void SendAlreadyRegisteredEmail(string email, string origin)
    {
        var message = !string.IsNullOrEmpty(origin)
            ? $@"<p>If you don't know your password please visit the <a href=""{origin}/account/forgot-password"">forgot password</a> page.</p>"
            : "<p>If you don't know your password you can reset it via the <code>/accounts/forgot-password</code> api route.</p>";
        _emailService.Send(
            email,
            "Sign-up Verification API - Email Already Registered",
            $@"<h4>Email Already Registered</h4>
                        <p>Your email <strong>{email}</strong> is already registered.</p>
                        {message}"
        );
    }
    private async Task<string> GenerateVerificationToken()
    {
        var token = Convert.ToHexString(RandomNumberGenerator.GetBytes(64));

        var account = await _accountRepository.GetAccountByVerificationToken(token);

        var tokenIsUnique = account == null;

        if (!tokenIsUnique)
            return await GenerateVerificationToken();
        return token;
    }
}