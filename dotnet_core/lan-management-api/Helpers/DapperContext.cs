using System.Data;
using Microsoft.Data.SqlClient;

namespace lan_management_api.Helpers;

public class DapperContext
{
    private readonly IConfiguration _configuration;

    public DapperContext(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public IDbConnection CreateConnection()
    {
        return new SqlConnection(_configuration.GetConnectionString("lan-management-database"));
    }
}