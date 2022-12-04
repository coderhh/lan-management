using System.ComponentModel.DataAnnotations;
using Microsoft.EntityFrameworkCore;

namespace lan_management_api.Entities;

[Owned]
public class RefreshToken
{
    [Key]
    public int Id { get; set; }
    public Account Account { get; set; }
    [MaxLength(64)]
    public string Token { get; set; }
    public DateTime Expires { get; set; }
    public DateTime Created { get; set; }
    [MaxLength(50)]
    public string CreatedByIp { get; set; }
    public DateTime? Revoked { get; set; }
    [MaxLength(50)]
    public string RevokedByIp { get; set; }
    [MaxLength(50)]
    public string ReplacedByIp { get; set; }
    [MaxLength(64)]
    public string ReplaceByToken { get; set; }
    [MaxLength(100)]
    public string ReasonRevoked { get; set; }
    public bool IsExpired => DateTime.UtcNow >= Expires;
    public bool IsRevoked => Revoked != null;
    public bool IsActive => Revoked == null && !IsExpired;
}