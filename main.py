#######################
# IMPORTS AND GLOBALS #
#######################

import os
import time
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
                file = getvideo(url)
                await ctx.send("Playing audio file...")
                if not isconnected(ctx):
                    await ctx.author.voice.channel.connect()
                if ctx.voice_client.is_playing():
                    ctx.voice_client.pause()
                ctx.voice_client.play(discord.FFmpegPCMAudio(file[0]))
            else:
                await ctx.send("Searching query...")
                # Get youtube search result as a link
                # actionplay(ctx, [search])
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


def getvideo(url):
    millis = time.time() * 1000
    console = (os.popen("youtube -o media/" + str(millis) + ".mp3 -x --audio-format mp3 " + url).read())
    return ["media/" + str(millis) + ".mp3", console]


def isconnected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client

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


client.run("OTA1MzgxOTk3NjU0OTgyNjc4.YYJQsQ.Ot_xz5O3y8kezG67rzc2K2bxfVE")
