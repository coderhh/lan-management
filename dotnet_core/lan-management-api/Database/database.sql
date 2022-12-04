use [lan-management-db]
go
DROP TABLE IF EXISTS dbo.RefreshToken;
DROP TABLE IF EXISTS dbo.Accounts;
create table Accounts
(
    Id                int identity(1,1)
        constraint PK_Accounts
            primary key,
    Title             nvarchar(50) not null,
    FirstName         nvarchar(50) not null,
    LastName          nvarchar(50) not null,
    Email             nvarchar(50) not null,
    PasswordHash      nvarchar(64) not null,
    AcceptTerms       bit          not null,
    Role              int          not null,
    VerificationToken nvarchar(128) not null,
    Verified          datetime2,
    ResetToken        nvarchar(64),
    ResetTokenExpires datetime2,
    Created           datetime2,
    Updated           datetime2,
    PasswordReset     datetime2
)
go

create table RefreshToken
(
    Id             int identity(1,1)
        constraint PK_RefreshToken
            primary key,
    AccountId      int          not null
        constraint FK_RefreshToken_Accounts_AccountId
            references Accounts
            on delete cascade,
    Token          nvarchar(64) not null,
    Expires        datetime2    not null,
    Created        datetime2    not null,
    CreatedByIp    nvarchar(50) not null,
    Revoked        datetime2,
    RevokedByIp    nvarchar(50) not null,
    ReplacedByIp   nvarchar(50) not null,
    ReplaceByToken nvarchar(64) not null,
    ReasonRevoked  nvarchar(100) not null
)
go

create index IX_RefreshToken_AccountId
    on RefreshToken (AccountId)
go


