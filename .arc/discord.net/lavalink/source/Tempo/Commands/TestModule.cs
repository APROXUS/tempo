using System.Threading.Tasks;
using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;

namespace Tempo.Commands
{
    #pragma warning disable CA1822 // Mark members as static

    public class TestModule : BaseCommandModule
    {
        [Command("ping")]
        public async Task Ping(CommandContext ctx)
        {
            await ctx.RespondAsync("[Tempo]: Pong!");
        }

        [Command("echo")]
        public async Task Echo(CommandContext ctx, [RemainingText]string arg)
        {
            await ctx.RespondAsync($"[Tempo]: *{arg}*");
        }
    }
}
