# Tempo (Discord Bot)

A simple Discord bot that plays online videos (YouTube and most publicly accessible streaming platforms) as audio in voice chat.

Tempo will work by initially downloading the audio of a YouTube (or other platform) video and then streaming the resulting audio file.

# Installation

1. Create ".env" file with the properties:
    - TOKEN=*Found in "Bot" section of Discord Developers website*
    - CLIENT_ID=*Found in "OAuth2" section of Discord Developers website*
    - GUILD_ID=*Right-click server icon and copy ID*

2. Run "install.sh" bash script (can be interpreted for other systems - made for Ubuntu).

3. Run "node index.js load" once to deploy slash commands.

4. See unit/README for information on deploying as an automatic service.