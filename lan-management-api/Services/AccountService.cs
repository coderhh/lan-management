using System.Security.Cryptography;
using lan_management_api.Helpers;

namespace lan_management_api.Services;

public class AccountService : IAccountService
{
    private readonly DataContext _context;
    private readonly IEmailService _emailService;
    private readonly IMapper _mapper;

    public AccountService(DataContext context, IEmailService emailService, IMapper mapper)
    {
        _context = context;
        _emailService = emailService;
        _mapper = mapper;
    }

    public void Register(RegisterRequest model, string origin)
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
        account.VerificationToken = GenerateVerificationToken();

        account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        _context.Accounts.Add(account);
        _context.SaveChanges();
    }

    public IEnumerable<AccountResponse> GetAll()
    {
        var accounts = _context.Accounts;
        return _mapper.Map<IList<AccountResponse>>(accounts);
    }

    public AccountResponse Create(CreateRequest model)
    {
        if (_context.Accounts.Any(x => x.Email == model.Email))
            throw new AppException($"Email '{model.Email}' is already registered");

        var account = _mapper.Map<Account>(model);
        account.Created = DateTime.UtcNow;
        account.Verified = DateTime.UtcNow;
        account.VerificationToken = GenerateVerificationToken();

        account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        _context.Accounts.Add(account);
        _context.SaveChanges();

        return _mapper.Map<AccountResponse>(account);
    }

    public AccountResponse GetById(int id)
    {
        var account = GetAccount(id);
        return _mapper.Map<AccountResponse>(account);
    }

    public void Delete(int id)
    {
        var account = GetAccount(id);
        _context.Accounts.Remove(account);
        _context.SaveChanges();
    }

    public AccountResponse Update(int id, UpdateRequest model)
    {
        var account = GetAccount(id);
        if (account.Email != model.Email && _context.Accounts.Any(x => x.Email == model.Email))
            throw new AppException($"Email '{model.Email}' is already registered");

        if (!string.IsNullOrEmpty(model.Password))
            account.PasswordHash = BCrypt.Net.BCrypt.HashPassword(model.Password);

        _mapper.Map(model, account);
        account.Updated = DateTime.UtcNow;
        _context.Accounts.Update(account);
        _context.SaveChanges();

        return _mapper.Map<AccountResponse>(account);
    }

    private Account GetAccount(int id)
    {
        var account = _context.Accounts.Find(id);
        if (account == null) throw new KeyNotFoundException("Account not found");
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

    private string GenerateVerificationToken()
    {
        var token = Convert.ToHexString(RandomNumberGenerator.GetBytes(64));

        var tokenIsUnique = !_context.Accounts.Any(x => x.VerificationToken == token);

        if (!tokenIsUnique)
            return GenerateVerificationToken();
        return token;
    }
}