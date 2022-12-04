using System.Text.Json;
using Microsoft.Extensions.Caching.Distributed;

namespace lan_management_api.Helpers;

public static class CacheHelper
{
    public static async Task SetRecordAsync<T>(this IDistributedCache cache,
        string recordId,
        T data,
        TimeSpan? slidingExpireTime = null,
        TimeSpan? absoluteExpireTime = null)
    {
        var options = new DistributedCacheEntryOptions();

        options.AbsoluteExpirationRelativeToNow = absoluteExpireTime ?? TimeSpan.FromSeconds(60);
        options.SlidingExpiration = slidingExpireTime;

        var jsonData = JsonSerializer.Serialize(data);
        await cache.SetStringAsync(recordId, jsonData, options);
    }

    public static async Task<T?> GetRecordAsync<T>(this IDistributedCache cache, string recordId)
    {
        var jsonDate = await cache.GetStringAsync(recordId);

        if (jsonDate is null)
        {
            return default(T);
        }

        return JsonSerializer.Deserialize<T>(jsonDate);
    }
}