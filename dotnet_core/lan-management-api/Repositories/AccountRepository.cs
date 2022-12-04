using System.Data;
using Dapper;
using lan_management_api.Helpers;
using Microsoft.Data.SqlClient;

namespace lan_management_api.Repositories;

public class AccountRepository : IAccountRepository
{
    private readonly IConfiguration _configuration;
    private readonly DapperContext _context;

    public AccountRepository(IConfiguration configuration, DapperContext context)
    {
        _configuration = configuration;
        _context = context;
    }
    public async Task<IEnumerable<Account>> GetAccountsByEmail(string email)
    {
        var sql = "SELECT * FROM accounts WHERE email = @Email";
        var parameters = new DynamicParameters();
        parameters.Add("Email", email, DbType.String);
        using var connection = _context.CreateConnection();
        var account = await connection.QueryAsync<Account>(sql, parameters);
        return account;
    }
    public async Task<Account> GetAccountById(int id)
    {
        var sql = "SELECT * FROM accounts WHERE Id = @Id";
        var parameters = new DynamicParameters();
        parameters.Add("Id", id, DbType.Int16);
        using var connection = _context.CreateConnection();
        var account = await connection.QueryFirstOrDefaultAsync<Account>(sql, parameters);
        return account;
    }
    public async Task<IEnumerable<Account>> GetAllAccounts()
    {
        var sql = "SELECT * FROM accounts";
        using var connection = new SqlConnection(_configuration.GetConnectionString("lan-management-database"));
        var accounts = await connection.QueryAsync<Account>(sql);
        return accounts;
    }
    public async Task<bool> UpdateAccount(Account account)
    {
        string sqlQuery = "UPDATE ACCOUNTS " +
                          "SET " +
                          "Title = @Title, " +
                          "FirstName = @FirstName, " +
                          "LastName = @LastName, " +
                          "Email = @Email, " +
                          "PasswordHash = @PasswordHash, " +
                          "AcceptTerms = @AcceptTerms, " +
                          "Role = @Role," +
                          "VerificationToken = @VerificationToken, " +
                          "Verified = @Verified," +
                          "ResetToken = @ResetToken, " +
                          "ResetTokenExpires = @ResetTokenExpires, " +
                          "Created = @Created, " +
                          "Updated = @Updated, " +
                          "PasswordReset = @PasswordReset WHERE Id = @Id";

        var parameters = new DynamicParameters();
        parameters.Add("Id", account.Id, DbType.String);
        parameters.Add("Title", account.Title, DbType.String);
        parameters.Add("FirstName", account.FirstName, DbType.String);
        parameters.Add("LastName", account.LastName, DbType.String);
        parameters.Add("Email", account.Email, DbType.String);
        parameters.Add("PasswordHash", account.PasswordHash, DbType.String);
        parameters.Add("AcceptTerms", account.AcceptTerms, DbType.String);
        parameters.Add("Role", account.Role, DbType.Boolean);
        parameters.Add("VerificationToken", account.VerificationToken, DbType.String);
        parameters.Add("Verified", account.Verified, DbType.DateTime2);
        parameters.Add("ResetToken", account.ResetToken, DbType.String);
        parameters.Add("ResetTokenExpires", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("Created", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("Updated", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("PasswordReset", account.PasswordReset, DbType.DateTime2);
        using var connection = _context.CreateConnection();
        var result = await connection.ExecuteAsync(sqlQuery, parameters);
        return result > 0;
    }
    public async Task<Account> GetAccountByVerificationToken(string token)
    {
        var sql = "SELECT * FROM accounts WHERE VerificationToken = @Token";
        var parameters = new DynamicParameters();
        parameters.Add("Token", token, DbType.String);
        using var connection = _context.CreateConnection();
        var account = await connection.QueryFirstOrDefaultAsync<Account>(sql, parameters);
        return account;
    }
    public async Task<bool> DeleteAllAccount()
    {
        var sql = "DELETE FROM Accounts;DBCC CHECKIDENT ('Accounts', RESEED, 0)";
        using var connection = _context.CreateConnection();
        var account = await connection.ExecuteAsync(sql);
        return account > 0;
    }
    public async Task<bool> DeleteAccountById(int id)
    {
        var sql = "DELETE FROM Accounts WHERE Id = @Id";
        var p = new DynamicParameters();
        p.Add("Id", id, DbType.Int16);
        using var connection = _context.CreateConnection();
        var account = await connection.ExecuteAsync(sql, p);
        return account > 0;
    }
    public async Task<Account> CreateAccount(Account account)
    {
        string sqlQuery = "INSERT INTO ACCOUNTS (" +
                          "Title, FirstName, " +
                          "LastName, Email, PasswordHash, " +
                          "AcceptTerms, Role, VerificationToken, " +
                          "Verified, ResetToken, ResetTokenExpires, " +
                          "Created, Updated, PasswordReset) " +
                          "VALUES " +
                          "(@Title, @FirstName, @LastName, " +
                          "@Email, @PasswordHash, @AcceptTerms, @Role, " +
                          "@VerificationToken, @Verified, @ResetToken, " +
                          "@ResetTokenExpires, @Created, @Updated, @PasswordReset)";

        var parameters = new DynamicParameters();
        parameters.Add("Title", account.Title, DbType.String);
        parameters.Add("FirstName", account.FirstName, DbType.String);
        parameters.Add("LastName", account.LastName, DbType.String);
        parameters.Add("Email", account.Email, DbType.String);
        parameters.Add("PasswordHash", account.PasswordHash, DbType.String);
        parameters.Add("AcceptTerms", account.AcceptTerms, DbType.String);
        parameters.Add("Role", account.Role, DbType.Boolean);
        parameters.Add("VerificationToken", account.VerificationToken, DbType.String);
        parameters.Add("Verified", account.Verified, DbType.DateTime2);
        parameters.Add("ResetToken", account.ResetToken, DbType.String);
        parameters.Add("ResetTokenExpires", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("Created", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("Updated", account.ResetTokenExpires, DbType.DateTime2);
        parameters.Add("PasswordReset", account.PasswordReset, DbType.DateTime2);
        using var connection = _context.CreateConnection();
        await connection.ExecuteAsync(sqlQuery, parameters);

        var selectQuery = "SELECT * FROM Accounts WHERE Email = @Email;";
        var p = new DynamicParameters();
        p.Add("Email", account.Email, DbType.String);
        var createdAccount = await connection.QuerySingleOrDefaultAsync<Account>(selectQuery, p);
        return createdAccount;
    }
}