namespace lan_management_api.Helpers;

public class AutoMapperProfile : Profile
{
    public AutoMapperProfile()
    {
        CreateMap<Account, AccountResponse>();
        CreateMap<CreateRequest, Account>();
        CreateMap<UpdateRequest, Account>()
            .ForAllMembers(x =>x.Condition(
                (src, des, prop) =>
                {
                    if (prop == null) return false;
                    if (prop is string && string.IsNullOrEmpty((string) prop)) return false;

                    if (x.DestinationMember.Name == "Role" && src.Role == null) return false;
                    return true;
                }));
    }
}