#######################
# IMPORTS AND GLOBALS #
#######################


import os
import re
import time
import urllib
import discord
import validators


from discord.utils import get
from discord.ext import commands


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
                    await ctx.send("Playing audio file...")
                    if not isconnected(ctx):
                        await ctx.author.voice.channel.connect()
                    if ctx.voice_client.is_playing():
                        ctx.voice_client.pause()
                    ctx.voice_client.play(discord.FFmpegPCMAudio(file[0]))
            else:
                await ctx.send("Searching query...")
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + "+".join(args))
                videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                await ctx.send("Found video: https://www.youtube.com/watch?v=" + videos[0])
                await actionplay(ctx, "https://www.youtube.com/watch?v=" + videos[0])
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


async def actionleave(ctx):
    if isconnected(ctx):
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not currently connected...")


def getvideo(ctx, url):
    millis = time.time() * 1000
    try:
        console = (os.popen("youtube -o media/" + str(millis) + ".mp3 -x --audio-format mp3 " + url).read())
        return["media/" + str(millis) + ".mp3", console]
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
async def leave(ctx):
    await actionleave(ctx)


@client.command()
async def l(ctx):
    await actionleave(ctx)


@client.command()
async def disconnect(ctx):
    await actionleave(ctx)


@client.command()
async def dc(ctx):
    await actionleave(ctx)


client.run(readconfig()[0])
