#######################
# IMPORTS AND GLOBALS #
#######################

import os
import re
import time
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
                await ctx.send("Retrieving video file...")
                file = getvideo(ctx, url)
                if file:
                    if len(queue) < 1:
                        queue.append(file[0])
                        await ctx.send("Playing audio file...")
                        await player(ctx)
                    else:
                        queue.append(file[0])
                        await ctx.send("Audio added to queue...")
                        await ctx.send("The queue has " + str(len(queue)) + " tracks...")
            else:
                await ctx.send("Searching query...")
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + "+".join(args[0]))
                videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                await ctx.send("Found video: https://www.youtube.com/watch?v=" + videos[0])
                await actionplay(ctx, ["https://www.youtube.com/watch?v=" + videos[0]])
        else:
            await ctx.send("You must enter a valid URL or search query...")
    else:
        await ctx.send("You must be connect to a voice channel...")


async def actionpause(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send("The bot is not currently playing...")
    else:
        await ctx.send("The bot is not currently connected...")


async def actionresume(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send("The bot is not currently paused...")
    else:
        await ctx.send("The bot is not currently connected...")


async def actionjoin(ctx):
    if isconnected(ctx):
        await ctx.send("The bot is already connected...")
    else:
        await ctx.author.voice.channel.connect()


async def actionleave(ctx):
    if isconnected(ctx):
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not currently connected...")


async def actionloop(ctx):
    global looping
    if looping:
        looping = False
        await ctx.send("The bot will not loop audio...")
    else:
        looping = True
        await ctx.send("The bot will loop audio...")


async def actionskip(ctx):
    if isconnected(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            if len(queue) > 0:
                await skipper(ctx)
            else:
                await ctx.send("There is no queue currently...")
        else:
            if len(queue) > 0:
                await skipper(ctx)
            else:
                await ctx.send("The bot is not currently playing...")
    else:
        await ctx.send("The bot is not currently connected...")


async def skipper(ctx):
    queue.pop(0)
    await player(ctx)
    await ctx.send("Skipping the current song...")


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
                queue.pop(0)
                if len(queue) < 1:
                    asyncio.run_coroutine_threadsafe(ctx.send("The que has been completed..."), client.loop)
                else:
                    asyncio.run_coroutine_threadsafe(
                        ctx.send("Playing next song (" + str(len(queue)) + " tracks left in queue)..."), client.loop)
                    asyncio.run_coroutine_threadsafe(player(ctx), client.loop)

        ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0]),
                              after=lambda e: asyncio.run_coroutine_threadsafe(loop(ctx, queue), client.loop))


def getvideo(ctx, url):
    millis = time.time() * 1000
    try:
        console = (os.popen("youtube -o media/" + str(millis) + ".mp3 -x --audio-format mp3 " + url).read())
        return ["media/" + str(millis) + ".mp3", console]
    except:
        ctx.send("The video could not be downloaded...")


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

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command()
async def echo(ctx, *args):
    await ctx.send(" ".join(args))


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


client.run(readconfig()[0])
