# PyCharm : discord.py
# Pycharm : youtube-dl2

import time
import youtube_dl
import validators

from discord.ext import commands

millis = time.time() * 1000
youtube = youtube_dl.YoutubeDL({'outtmpl': str(millis) + '.media'})
client = commands.Bot(command_prefix="!")

def getvideo(url):
    with youtube:
        result = youtube.extract_info(url, download=True)

    if 'entries' in result:
        video = result['entries'][0]
    else:
        video = result

    print(video)
    video_url = video['url']
    print(video_url)
    return video

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def echo(ctx, *args):
    await ctx.send(" ".join(args))

@client.command()
async def play(ctx, *args):
    if (args):
        if (validators.url(args[0])):
            await ctx.send("Found video, downloading...")
            getvideo(args[0])
            await ctx.send("Now playing: ###...")
        else:
            await ctx.send("Searching YouTube for: " + " ".join(args))
    else:
        await ctx.send("Please enter a URL or search query...")


client.run("OTA1MzgxOTk3NjU0OTgyNjc4.YYJQsQ.Ot_xz5O3y8kezG67rzc2K2bxfVE")
