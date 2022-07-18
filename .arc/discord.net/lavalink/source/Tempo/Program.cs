using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using DSharpPlus;
using DSharpPlus.Net;
using DSharpPlus.Lavalink;
using DSharpPlus.CommandsNext;
using Tempo.Commands;

namespace Tempo
{
    class Program
    {
        internal static async Task Main()
        {
            #region Start DSharpPlus client...
            DotNetEnv.Env.Load();

            var discord = new DiscordClient(new DiscordConfiguration()
            {
                Token = Environment.GetEnvironmentVariable("TOKEN"),
                TokenType = TokenType.Bot,
                Intents = DiscordIntents.AllUnprivileged,
                MinimumLogLevel = LogLevel.Debug,
                LogTimestampFormat = "MMM dd yyyy - hh:mm:ss tt",
            });

            var commands = discord.UseCommandsNext(new CommandsNextConfiguration()
            {
                StringPrefixes = new[] { "!" }
            });

            commands.RegisterCommands<TestModule>();
            commands.RegisterCommands<MusicModule>();

            var endpoint = new ConnectionEndpoint
            {
                Hostname = "127.0.0.1",
                Port = 2333
            };

            var config = new LavalinkConfiguration
            {
                Password = "tempofastorslow",
                RestEndpoint = endpoint,
                SocketEndpoint = endpoint
            };

            var lavalink = discord.UseLavalink();

            await discord.ConnectAsync();

            await lavalink.ConnectAsync(config);

            await Task.Delay(-1);
            #endregion
        }
    }
}
