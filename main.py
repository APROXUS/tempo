#######################
# IMPORTS AND GLOBALS #
#######################
import os
import re
import time
import glob
import urllib
import asyncio
import discord
import validators

from discord.utils import get
from discord.ext import commands

import tracemalloc

tracemalloc.start()

queue = []
looping = False
client = commands.Bot(command_prefix="!")


####################
# ACTION FUNCTIONS #
####################

async def actionplay(ctx, args):
    if ctx.author.voice is not None:
        if args:
            url = str(args[0])
            if validators.url(url):
                if re.findall(r"playlist\?list=(\S{34})", url):
                    await getplaylist(ctx, re.findall(r"playlist\?list=(\S{34})", url)[0])
                else:
                    await ctx.send("[Player]: Retrieving track...")
                    file = getvideo(ctx, url)
                    if file:
                        if len(queue) < 1:
                            queue.append(file[0])
                            await ctx.send("[Player]: Playing track...")
                            await player(ctx)
                        else:
                            queue.append(file[0])
                            await ctx.send("[Queue]: Track added...")
                            await ctx.send("[Queue]: Playing " + str(len(queue)) + " tracks...")
            else:
                await ctx.send("[Search]: Querying YouTube...")
                query = "https://www.youtube.com/results?search_query=" + "+".join(args)
                html = urllib.request.urlopen(query)
                videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                await ctx.send("[Search]: Found https://www.youtube.com/watch?v=" + videos[0])
                await actionplay(ctx, ["https://www.youtube.com/watch?v=" + videos[0]])
        else:
            await ctx.send("[Error]: Must have a URL or search arguments...")
    else:
        await ctx.send("[Error]: Must be connect to a voice channel...")


async def actionpause(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send("[Error]: Not currently playing...")
    else:
        await ctx.send("[Error]: The bot is not connected...")


async def actionresume(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send("[Error]: Not currently paused...")
    else:
        await ctx.send("[Error]: The bot is not connected...")


async def actionjoin(ctx):
    if isconnected(ctx):
        await ctx.send("[Error]: The bot is already connected...")
    else:
        await ctx.author.voice.channel.connect()


async def actionleave(ctx):
    if isconnected(ctx):
        global queue
        queue = []
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("[Error]: The bot is not connected...")


async def actionloop(ctx):
    global looping
    if looping:
        looping = False
        await ctx.send("[Player]: No longer looping tracks...")
    else:
        looping = True
        await ctx.send("[Player]: Now looping tracks...")


async def actionremove(ctx, arg):
    if arg.isdigit():
        if int(arg) <= len(queue):
            if int(arg) == 1:
                await actionskip(ctx)
            else:
                queue.pop(int(arg)-1)
                await ctx.send("[Queue]: Removed track " + arg + "...")
        else:
            await ctx.send("[Error]: Track number does not exist...")
    else:
        await ctx.send("[Error]: Argument is not an integer...")


async def actionskip(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            if len(queue) > 0:
                await skipper(ctx)
            else:
                await ctx.send("[Error]: There is no active queue...")
        else:
            if len(queue) > 0:
                await skipper(ctx)
            else:
                await ctx.send("[Error]: The bot is not playing...")
    else:
        await ctx.send("[Error]: The bot is not connected...")


async def skipper(ctx):
    queue.pop(0)
    await ctx.send("[Player]: Skipping track (" + str(len(queue)) + " tracks in queue)...")
    await player(ctx)


async def player(ctx):
    if len(queue) > 0:
        if not isconnected(ctx):
            await ctx.author.voice.channel.connect()
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()

        def loop(ctx, queue):
            if looping:
                ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0]), after=lambda e: asyncio.run_coroutine_threadsafe(loop(ctx, queue), client.loop))
            else:
                remove(queue[0])
                queue.pop(0)
                if len(queue) < 1:
                    asyncio.run_coroutine_threadsafe(ctx.send("[Player]: Queue completed..."), client.loop)
                else:
                    asyncio.run_coroutine_threadsafe(
                        ctx.send("[Player]: Playing next track (" + str(len(queue)) + " tracks in queue)..."), client.loop)
                    asyncio.run_coroutine_threadsafe(player(ctx), client.loop)

        ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0]),
                              after=lambda e: asyncio.run_coroutine_threadsafe(loop(ctx, queue), client.loop))


def getvideo(ctx, url):
    file = re.findall(r"watch\?v=(\S{11})", url)

    if len(file) > 0:
        file = file[0]
    else:
        file = time.time() * 1000

    path = "media/"
    exists = glob.glob(path + file + ".mp3", recursive=True)
    if len(exists) > 0:
        return ["media/" + str(file) + ".mp3", "File already cached locally..."]

    try:
        console = (os.popen("yt-dlp -o media/" + str(file) + ".mp3 -x --audio-format mp3 " + url).read())
        return ["media/" + str(file) + ".mp3", console]
    except:
        ctx.send("[Error]: Could not retrieve track...")


async def getplaylist(ctx, arg):
    await ctx.send("[Search]: Detected playlist...")
    html = urllib.request.urlopen("https://www.youtube.com/playlist?list=" + arg)
    videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    videos = list(dict.fromkeys(videos))
    await ctx.send("[Search]: Queueing all " + str(len(videos)) + " tracks...")
    for i in range(len(videos)):
        await actionplay(ctx, ["https://www.youtube.com/watch?v=" + videos[i]])


def isconnected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client


def readconfig():
    file = open(".config", "r")
    lines = file.read().splitlines()
    file.close()
    return lines


###################
# COMMAND HANDLER #
###################

client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command()
async def echo(ctx, *args):
    await ctx.send(" ".join(args))


@client.command()
async def help(ctx):
    await ctx.send("No!")

@client.command()
async def play(ctx, *args):
    await actionplay(ctx, args)


@client.command()
async def p(ctx, *args):
    await actionplay(ctx, args)


@client.command()
async def pause(ctx):
    await actionpause(ctx)


@client.command()
async def stop(ctx):
    await actionpause(ctx)


@client.command()
async def resume(ctx):
    await actionresume(ctx)


@client.command()
async def r(ctx):
    await actionresume(ctx)


@client.command()
async def join(ctx):
    await actionjoin(ctx)


@client.command()
async def leave(ctx):
    await actionleave(ctx)


@client.command()
async def disconnect(ctx):
    await actionleave(ctx)


@client.command()
async def dc(ctx):
    await actionleave(ctx)


@client.command()
async def loop(ctx):
    await actionloop(ctx)


@client.command()
async def l(ctx):
    await actionloop(ctx)


@client.command()
async def repeat(ctx):
    await actionloop(ctx)


@client.command()
async def skip(ctx):
    await actionskip(ctx)


@client.command()
async def s(ctx):
    await actionskip(ctx)


@client.command()
async def fs(ctx):
    await actionskip(ctx)


@client.command()
async def remove(ctx, arg):
    await actionremove(ctx, arg)


@client.command()
async def rm(ctx, arg):
    await actionremove(ctx, arg)


@client.command()
async def delete(ctx, arg):
    await actionremove(ctx, arg)


@client.command()
async def d(ctx, arg):
    await actionremove(ctx, arg)

@client.command()
async def cache(ctx, arg):
    await actioncache(ctx)

@client.command()
async def cached(ctx, arg):
    await actioncache(ctx)

@client.command()
async def data(ctx, arg):
    await actioncache(ctx)

@client.command()
async def purge(ctx, arg):
    await actionpurge(ctx)


client.run(readconfig()[0])
