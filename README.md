# Conducter

*(Discord, Discord.NET, DSharpPlus, Lavalink)*

KPNC Technology: Conducter: A simple Discord bot that plays online videos (YouTube and most streaming platforms) as audio in voice chat.

# Installation

*For installation on a linux (Debian based) server...*

1. Install necessary base dependencies:
	- Run "sudo bash install.sh"
	
1. Duplicate or rename ".env.example" to ".env" and edit the following properties:
    - TOKEN *(Change to your Discord Bot token from the Discord Developers website...)*
	- PREFIX *(Change to any prefered string to activate the bot like "!", "~", "#", "$", "bot>", etc...)*
	- OWNER_ID *(Change to your own Discord ID (right click your name in Discord app)...)*
	- LAVA_HOST *(Change to a public Lavalink server host name if you do not want to self-host...)*
	- LAVA_PORT *(Change to a public Lavalink server port if you do not want to self-host...)*
	- LAVA_PASS *(Change to a public Lavalink server password if you do not want to self-host...)*
	- ENABLE_SPOTIFY *(Change to "true" if you want to stream from Spotify...)*
	- SPOTIFY_ID *(Change to your personal Spotify ID if you enabled Spotify support...)*
	- SPOTIFY_SECRET *(Change to your personal Spotify secret if you enabled Spotify support...)*

3. Finally create the service files, see unit/readme for more information...
