namespace lan_management_api.Entities;

public class Account
{
    [Key]
    public int Id { get; set; }
    [MaxLength(50)]
    public string Title { get; set; }
    [MaxLength(50)]
    public string FirstName { get; set; }
    [MaxLength(50)]
    public string LastName { get; set; }
    [MaxLength(50)]
    public string Email { get; set; }
    [MaxLength(64)]
    public string PasswordHash { get; set; }
    public bool AcceptTerms { get; set; }
    public Role Role { get; set; }
    [MaxLength(128)]
    public string VerificationToken { get; set; }
    public DateTime? Verified { get; set; }
    public bool IsVerified => Verified.HasValue || PasswordReset.HasValue;
    [MaxLength(64)]
    public string ResetToken { get; set; }
    public DateTime? ResetTokenExpires { get; set; }
    public DateTime? Created { get; set; }
    public DateTime? Updated { get; set; }
    public List<RefreshToken> RefreshTokens { get; set; }
    public DateTime? PasswordReset { get; set; }
    public bool OwnsToken(string token)
    {
        return RefreshTokens?.Find(x => x.Token == token) != null;
    }
}