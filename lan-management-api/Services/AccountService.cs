using System.Security.Cryptography;
using lan_management_api.Entities;
using lan_management_api.Helpers;
using lan_management_api.Models.Accounts;
using AutoMapper;

namespace lan_management_api.Services;

public class AccountService: IAccountService
{
    private readonly DataContext _context;
    private readonly IMapper _mapper;
    public AccountService(DataContext context)
    {
        _context = context;
    }
    public void Register(RegisterRequest model, string origin)
    {
        if (_context.Accounts.Any(x => x.Email == model.Email))
        {
            //TODO send already registered error in email to prevent account enumeration
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

    private string GenerateVerificationToken()
    {
        var token = Convert.ToHexString(RandomNumberGenerator.GetBytes(64));

        var tokenIsUnique = !_context.Accounts.Any(x => x.VerificationToken == token);

        if (!tokenIsUnique)
            return GenerateVerificationToken();
        return token;
    }
}

public interface IAccountService
{
    void Register(RegisterRequest model, string origin);
}