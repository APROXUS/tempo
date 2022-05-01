using System;
using System.Threading;
using System.Reflection;
using System.Threading.Tasks;

using Discord;
using Discord.Commands;
using Discord.WebSocket;
using Discord.Addons.Hosting;

using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;

namespace Tempo.Services
{
    public class CommandHandler : DiscordClientService
    {
        private readonly IServiceProvider provider;
        private readonly CommandService service;
        private readonly IConfiguration config;

        public CommandHandler(DiscordSocketClient client, ILogger<CommandHandler> logger, IServiceProvider provider, CommandService service, IConfiguration config) : base(client, logger)
        {
            this.provider = provider;
            this.service = service;
            this.config = config;
        }
        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            Client.MessageReceived += HandleMessage;
            service.CommandExecuted += CommandExecutedAsync;
            await service.AddModulesAsync(Assembly.GetEntryAssembly(), provider);
        }

        private async Task HandleMessage(SocketMessage incomingMessage)
        {
            if (incomingMessage is not SocketUserMessage message) return;
            if (message.Source != MessageSource.User) return;

            int argPos = 0;
            if (!message.HasStringPrefix(config["Prefix"], ref argPos) && !message.HasMentionPrefix(Client.CurrentUser, ref argPos)) return;

            var context = new SocketCommandContext(Client, message);
            await service.ExecuteAsync(context, argPos, provider);
        }

        public async Task CommandExecutedAsync(Optional<CommandInfo> command, ICommandContext context, IResult result)
        {
            Logger.LogInformation("User {user} attempted to use command {command}", context.User, command.Value.Name);

            if (!command.IsSpecified || result.IsSuccess) return;

            await context.Channel.SendMessageAsync($"[Tempo]: Error: {result}");
        }
    }
}
