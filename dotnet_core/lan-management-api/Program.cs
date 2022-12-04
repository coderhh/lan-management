using System.Text.Json.Serialization;
using lan_management_api.Helpers;
using lan_management_api.Repositories;

namespace lan_management_api;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        var services = builder.Services;
        // Add services to the container.

        services.AddControllers();
        // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
        services.AddEndpointsApiExplorer();
        services.AddSwaggerGen();
        services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());


        services.AddDbContext<DataContext>();
        services.AddSingleton<DapperContext>();
        services.AddCors();
        services.AddControllers().AddJsonOptions(x =>
        {
            x.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
        });
        services.AddScoped<IAccountService, AccountService>();
        services.AddScoped<IEmailService, EmailService>();
        services.AddScoped<IAccountRepository, AccountRepository>();
        var app = builder.Build();

        // Configure the HTTP request pipeline.
        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();

        app.UseAuthorization();


        app.MapControllers();

        app.Run();
    }
}