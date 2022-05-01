using System;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Collections.Concurrent;
using DSharpPlus;
using DSharpPlus.Lavalink;
using DSharpPlus.Entities;
using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;

namespace Tempo.Commands
{
    #pragma warning disable CA1822 // Mark members as static

    public class MusicModule : BaseCommandModule
    {
        static readonly ConcurrentDictionary<ulong, List<string>> queue;
        static readonly ConcurrentDictionary<ulong, bool> loop;

        #region Command Logic...
        [Command("join")]
        public async Task Join(CommandContext ctx, bool silent = false)
        {
            if (ctx.Member.VoiceState == null || ctx.Member.VoiceState.Channel == null)
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Must be in a voice channel...");
                return;
            }

            DiscordChannel channel = ctx.Member.VoiceState.Channel;

            var lava = ctx.Client.GetLavalink();

            await Leave(ctx, true);

            if (!lava.ConnectedNodes.Any())
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Could not establish Lavalink connection...");
                return;
            }

            var node = lava.ConnectedNodes.Values.First();

            if (channel.Type != ChannelType.Voice)
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Not a valid voice channel...");
                return;
            }

            await node.ConnectAsync(channel);
        }

        [Command("leave")]
        public async Task Leave(CommandContext ctx, bool silent = false)
        {
            if (ctx.Member.VoiceState == null || ctx.Member.VoiceState.Channel == null)
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Must be in a voice channel...");
                return;
            }

            DiscordChannel channel = ctx.Member.VoiceState.Channel;

            var lava = ctx.Client.GetLavalink();

            if (!lava.ConnectedNodes.Any())
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Could not establish Lavalink connection...");
                return;
            }

            var node = lava.ConnectedNodes.Values.First();

            if (channel.Type != ChannelType.Voice)
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Not a valid voice channel...");
                return;
            }

            var conn = node.GetGuildConnection(channel.Guild);

            if (conn == null)
            {
                if (!silent) await ctx.RespondAsync("[Tempo]: Currently not connected...");
                return;
            }

            await conn.DisconnectAsync();
        }

        [Command("play")]
        public async Task Play(CommandContext ctx, [RemainingText] string search)
        {
            await Add(ctx, search);
        }

        [Command("pause")]
        public async Task Pause(CommandContext ctx)
        {
            if (ctx.Member.VoiceState == null || ctx.Member.VoiceState.Channel == null)
            {
                await ctx.RespondAsync("[Tempo]: Must be in a voice channel...");
                return;
            }

            var lava = ctx.Client.GetLavalink();
            var node = lava.ConnectedNodes.Values.First();
            var conn = node.GetGuildConnection(ctx.Member.VoiceState.Guild);

            if (conn == null)
            {
                await ctx.RespondAsync("[Tempo]: Currently not connected...");
                return;
            }

            if (conn.CurrentState.CurrentTrack == null)
            {
                await ctx.RespondAsync("[Tempo]: There are no tracks loaded...");
                return;
            }

            await conn.PauseAsync();
        }

        [Command("resume")]
        public async Task Resume(CommandContext ctx)
        {
            if (ctx.Member.VoiceState == null || ctx.Member.VoiceState.Channel == null)
            {
                await ctx.RespondAsync("[Tempo]: Must be in a voice channel...");
                return;
            }

            var lava = ctx.Client.GetLavalink();
            var node = lava.ConnectedNodes.Values.First();
            var conn = node.GetGuildConnection(ctx.Member.VoiceState.Guild);

            if (conn == null)
            {
                await ctx.RespondAsync("[Tempo]: Currently not connected...");
                return;
            }

            if (conn.CurrentState.CurrentTrack == null)
            {
                await ctx.RespondAsync("[Tempo]: There are no tracks loaded...");
                return;
            }

            await conn.ResumeAsync();
        }

        [Command("loop")]
        public async Task Loop(CommandContext ctx)
        {
            bool looping = true;

            if (loop.TryGetValue(ctx.Guild.Id, out bool l))
            {
                looping = !l;
            }

            loop.AddOrUpdate(ctx.Guild.Id, looping, (key, value) => looping);

            await ctx.RespondAsync($"[Tempo]: Looping was set to {looping}...");
        }

        [Command("skip")]
        public async void Skip(CommandContext ctx)
        {
            if (queue[ctx.Guild.Id].Count < 2)
            {
                queue.Remove(ctx.Guild.Id, out List<string> _);

                await ctx.RespondAsync("[Tempo]: No queries in queue...");
                return;
            }
            else
            {
                if (queue.TryGetValue(ctx.Guild.Id, out List<string> searches))
                {
                    searches.RemoveAt(0);

                    queue.AddOrUpdate(ctx.Guild.Id, searches, (key, value) => searches);
                }

                await Player(ctx);
            }
        }

        [Command("queue")]
        public async Task Queue(CommandContext ctx)
        {
            if (queue.TryGetValue(ctx.Guild.Id, out List<string> searches))
            {
                List<string> message = new() { "[Tempo]: The current query queue is:" };

                foreach (string search in searches) message.Add(">" + search);

                string whole = String.Join("\n", message.ToArray());

                await ctx.RespondAsync(whole);
            }
            else
            {
                await ctx.RespondAsync($"[Tempo]: There is no query queue...");
            }
        }
        #endregion

        #region Queue Logic...
        private async Task Player(CommandContext ctx)
        {
            string search;

            if (queue.TryGetValue(ctx.Guild.Id, out List<string> s))
            {
                search = s.First();
            }
            else
            {
                await ctx.RespondAsync("[Tempo]: No queries in queue...");
                return;
            }

            if (ctx.Member.VoiceState == null || ctx.Member.VoiceState.Channel == null)
            {
                await ctx.RespondAsync("[Tempo]: Must be in a voice channel...");
                return;
            }

            var lava = ctx.Client.GetLavalink();
            var node = lava.ConnectedNodes.Values.First();
            var conn = node.GetGuildConnection(ctx.Member.VoiceState.Guild);

            if (conn == null)
            {
                await Join(ctx, true);

                conn = node.GetGuildConnection(ctx.Member.VoiceState.Guild);

                if (conn == null)
                {
                    await ctx.RespondAsync("[Tempo]: Could not connect to channel...");
                    return;
                }
            }

            var loadResult = await node.Rest.GetTracksAsync(search);

            if (loadResult.LoadResultType == LavalinkLoadResultType.LoadFailed || loadResult.LoadResultType == LavalinkLoadResultType.NoMatches)
            {
                await ctx.RespondAsync($"[Tempo]: Track search failed for {search}...");
                return;
            }

            var track = loadResult.Tracks.First();

            await conn.PlayAsync(track);

            await ctx.RespondAsync($"[Tempo]: Now playing {track.Title}...");

            conn.PlaybackFinished += async (s, e) =>
            {
                await Completed(ctx);
            };
        }

        private async Task Completed(CommandContext ctx)
        {
            if (loop[ctx.Guild.Id])
            {
                await Player(ctx);
            }
            else if (queue[ctx.Guild.Id].Count < 2)
            {
                queue.Remove(ctx.Guild.Id, out List<string> _);

                await ctx.RespondAsync("[Tempo]: No queries in queue...");
                return;
            }
            else
            {
                if (queue.TryGetValue(ctx.Guild.Id, out List<string> searches))
                {
                    searches.RemoveAt(0);

                    queue.AddOrUpdate(ctx.Guild.Id, searches, (key, value) => searches);
                }

                await Player(ctx);
            }
        }

        private async Task Add(CommandContext ctx, string search)
        {
            List<string> searches = new() { search };

            if (queue.TryGetValue(ctx.Guild.Id, out List<string> s))
            {
                searches = s;

                searches.Add(search);
            }

            queue.AddOrUpdate(ctx.Guild.Id, new List<string> { search }, (key, value) => searches);

            await ctx.RespondAsync($"[Tempo]: Added '{search}' query to queue...");

            if (queue[ctx.Guild.Id].Count < 2)
            {
                await Player(ctx);
            }
        }
        #endregion
    }
}