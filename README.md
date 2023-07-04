# Conducter

*(Node.js, Discord.js, YT-DLP)*

KPNC Technology: Conducter: is a simple Discord music bot that utilizes the popular Discord.js and Youtube-DL projects. Installing your own version of Conducter is easy and only requires that you have an computer and a Discord account.

# Installation

__*For installation on a Linux (Ubuntu based) servers...*__

- Install necessary base dependencies:
	- Run "sudo bash install.sh"

- Duplicate or rename ".env.example" to ".env" and edit the following properties:
	- TOKEN ( Your bot's Token... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- CLIENT_ID ( Your bot's Client ID... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- GUILD_ID ( Your server's Guild ID... [Tutorial](https://support.discord.com/hc/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) )

- Finally create the service files, see unit/readme for more information...

__*For installation on a Windows (10/2019+) servers...*__

- Install [Node.js](https://nodejs.org/en/download) (this will also install [NPM](https://www.npmjs.com/))

- Install necessary Node dependencies:
	- Run "npm i --production"
	
- Duplicate or rename ".env.example" to ".env" and edit the following properties:
	- TOKEN ( Your bot's Token... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- CLIENT_ID ( Your bot's Client ID... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- GUILD_ID ( Your server's Guild ID... [Tutorial](https://support.discord.com/hc/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) )

- If you would like the program to automatically start:
	- Create shortcut of "start.bat" by right-clicking and selecting "Create Shortcut"
	- You can rename this shortcut to whatever you want
	- Move the shortcut to the "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp" directory

# Operation 

__*Covering both Linux and Windows environments...*__

- Invite your bot to server(s)... [Tutorial](https://discordjs.guide/preparations/adding-your-bot-to-servers.html)
- After adding your bot to any servers, you must register your slash commands by running "node deploy.js"
- Start your bot:
	- On Linux run "sudo service conducter start"
	- On Windows open the "Start.bat" script
- Bot status:
	- On Linux run "sudo service conducter status"
	- On Windows bring your Node/CMD window to the foreground
- Stop your bot:
	- On Linux run "sudo service conducter stop"
	- On Windows close the Node/CMD window
- Discord Commands:
	- /play: Plays the linked (or searched) YouTube audio
	- /skip: Skips the current song
	- /pause: Pauses music playback
	- /resume: Resumes music playback
	- /stop: Disconnects the bot and resets audio state
	- /about: Displays an overview of Conducter
	- /ping: Tests your slash command