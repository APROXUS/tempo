using System.Threading;
using System.Threading.Tasks;

using Discord;
using Discord.WebSocket;
using Discord.Addons.Hosting;
using Discord.Addons.Hosting.Util;

using Microsoft.Extensions.Logging;

namespace Tempo.Services
{
    public class StatusService : DiscordClientService
    {
        public StatusService(DiscordSocketClient client, ILogger<DiscordClientService> logger) : base(client, logger) { }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            await Client.WaitForReadyAsync(stoppingToken);
            Logger.LogInformation("Client is ready!");

            await Client.SetActivityAsync(new Game("'$help' for more info..."));
        }
    }
}