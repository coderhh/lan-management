using Microsoft.EntityFrameworkCore;

namespace lan_management_api.Helpers;

public sealed class DataContext : DbContext
{
    private readonly IConfiguration _configuration;

    public DataContext(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public DbSet<Account> Accounts { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        //options.UseSqlite(_configuration.GetConnectionString("lan-management-database"));
        options.UseSqlServer(_configuration.GetConnectionString("lan-management-database"));
    }
}