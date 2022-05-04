# Tempo (Discord Bot)

A simple Discord bot that plays online videos (YouTube and most publicly accessible streaming platforms) as audio in voice chat.

Tempo will work by initially downloading the audio of a YouTube (or other platform) video and then streaming the resulting audio file.

# Installation

0. Working directory (default for configurations): /home/*user*/tempo/prod/

1. Create ".env" file with the properties:
    - TOKEN=*Found in "Bot" section of Discord Developers website*

2. Run "install.sh" bash script (can be interpreted for other systems - made for Ubuntu).

3. Finally create the service files, see unit/README for more information...

*If you want to use with Windows, install .NET 6 and JDK 13. Run both prod/Lavalink.jar and prod/Tempo.exe concurrently.