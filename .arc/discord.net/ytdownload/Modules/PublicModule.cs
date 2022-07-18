using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Collections.Concurrent;

using Discord;
using Discord.Audio;
using Discord.Commands;

using Microsoft.Extensions.Logging;

namespace Tempo.Modules
{
    public class PublicModule : ModuleBase<SocketCommandContext>
    {
        private readonly static ConcurrentDictionary<ulong, IAudioClient> ConnectedChannels = new();

        private readonly List<string> queue = new();
        private readonly ILogger<PublicModule> logger;
        private readonly string temp = "cache";

        static private bool looping;

        public PublicModule(ILogger<PublicModule> logger)
        {
            this.logger = logger;
        }

        //[Command("help")]
        //[Alias("h", "?")]
        //public async Task Help()
        //{

        //}

        [Command("ping")]
        public async Task Ping()
        {
            logger.LogInformation("User {user} used the ping command!", Context.User.Username);
            await ReplyAsync("[Tempo]: Pong!");
        }

        [Command("echo")]
        public async Task Echo([Remainder]string args)
        {
            logger.LogInformation("User {user} used the echo command!", Context.User.Username);
            await ReplyAsync("[Tempo]: " + args);
        }

        [Command("play", RunMode = RunMode.Async)]
        [Alias("p")]
        public async Task Play(string args)
        {
            logger.LogInformation("User {user} used the play command ({song})!", Context.User.Username, args);

            queue.Add(args);

            await ReplyAsync($"[Tempo]: Added {args} to the queue!");

            await Task.Run(() => Player());
        }

        private async Task Player()
        {
            IAudioClient audio;

            logger.LogInformation("User {user} used the play command ({song})!", Context.User.Username, queue[0]);

            if (!File.Exists(queue[0]))
            {
                await ReplyAsync("[Tempo]: Could not find: " + queue[0]);
                return;
            }

            if (ConnectedChannels.TryGetValue(Context.Guild.Id, out IAudioClient client))
            {
                audio = client;
            }
            else
            {
                IVoiceChannel channel;
                channel = (Context.User as IGuildUser)?.VoiceChannel;
                if (channel == null)
                {
                    await ReplyAsync("[Tempo]: Join a channel...");
                    return;
                }

                audio = await channel.ConnectAsync();

                if (ConnectedChannels.TryAdd(Context.Guild.Id, audio))
                {
                    logger.LogInformation("Bot joined {guild}!", Context.Guild.Name);
                }
            }

            await ReplyAsync($"[Tempo]: Now playing {queue[0]}!");

            using var ffmpeg = CreateStream(queue[0]);
            using var output = ffmpeg.StandardOutput.BaseStream;
            using var discord = audio.CreatePCMStream(AudioApplication.Music);
            try { await output.CopyToAsync(discord); }
            finally { await discord.FlushAsync(); }

            Thread.Sleep(1000);

            if (looping) { await Task.Run(() => Player()); }
            else if (queue.Count > 2) { queue.RemoveAt(0); await ReplyAsync($"[Tempo]: Completed queue..."); }
            else { queue.RemoveAt(0); await Task.Run(() => Player()); }

            return;
        }

        private static Process CreateStream(string path)
        {
            return Process.Start(new ProcessStartInfo
            {
                FileName = "FFmpeg",
                Arguments = $"-hide_banner -loglevel panic -i \"{path}\" -ac 2 -f s16le -ar 48000 pipe:1",
                UseShellExecute = false,
                RedirectStandardOutput = true
            });
        }

        //[Command("pause")]
        //[Alias("stop")]
        //public async Task Pause()
        //{

        //}

        //[Command("resume")]
        //[Alias("start")]
        //public async Task Resume()
        //{

        //}

        [Command("join", RunMode = RunMode.Async)]
        public async Task Join(IVoiceChannel channel = null)
        {
            logger.LogInformation("User {user} used the join command in {guild}!", Context.User.Username, Context.Guild.Name);

            channel ??= (Context.User as IGuildUser)?.VoiceChannel;
            if (channel == null) {
                await Context.Channel.SendMessageAsync("[Tempo]: Join a channel or pass an argument...");
                return;
            }

            var audio = await channel.ConnectAsync();

            if (ConnectedChannels.TryAdd(Context.Guild.Id, audio))
            {
                logger.LogInformation("Bot joined {guild}!", Context.Guild.Name);
            }
        }

        [Command("leave")]
        [Alias("disconnect", "dc")]
        public async Task Leave()
        {
            logger.LogInformation("User {user} used the leave command in {guild}!", Context.User.Username, Context.Guild.Name);

            if (ConnectedChannels.TryRemove(Context.Guild.Id, out IAudioClient client))
            {
                await Task.Run(() => { client.Dispose(); });
            }
        }

        [Command("loop")]
        [Alias("repeat", "l")]
        public async Task Loop()
        {
            logger.LogInformation("User {user} used the loop command!", Context.User.Username);

            looping = !looping;

            if (looping) { await ReplyAsync("[Tempo]: Now looping..."); }
            else { await ReplyAsync("[Tempo]: No longer looping..."); }
        }

        //[Command("skip")]
        //[Alias("s", "fs")]
        //public async Task Skip()
        //{

        //}

        //[Command("remove")]
        //[Alias("rm", "delete", "d")]
        //public async Task Remove(string[] args)
        //{

        //}

        [Command("cache")]
        [Alias("cached", "data")]
        public async Task Cache()
        {
            logger.LogInformation("User {user} used the cache command!", Context.User.Username);

            Directory.CreateDirectory(temp);
            DirectoryInfo info = new(temp);
            long size = await Task.Run(() => info.EnumerateFiles("*", SearchOption.AllDirectories).Sum(file => file.Length));
            double mb = Math.Round(Convert.ToDouble(size) / 1024.0 / 1024.0, 2);

            logger.LogInformation("Using about {size} bytes of disk for cache!", size);
            await ReplyAsync($"[Tempo]: Cached about {mb} megabytes of audio...");
        }

        [Command("purge")]
        [RequireOwner]
        public async Task Purge()
        {
            logger.LogInformation("User {user} used the purge command!", Context.User.Username);

            Directory.CreateDirectory(temp);
            DirectoryInfo info = new(temp);
            foreach (FileInfo file in info.GetFiles()) { file.Delete(); }
            foreach (DirectoryInfo dir in info.GetDirectories()) { dir.Delete(true); }

            await ReplyAsync($"[Tempo]: Cache has been purged...");
        }
    }
}