namespace lan_management_api.Services;

public interface IEmailService
{
    void Send(string to, string subject, string html, string from = null);
}