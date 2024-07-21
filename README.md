# Virtuoso

*(Node.js, Discord.js, YT-DLP)*

KPNC Technology: Virtuoso is a simple music bot for Discord. It utilizes the popular Discord.js and YT-DLP libraries to play YouTube audio in your Discord server. Starting your own instance of Virtuoso is easy and only requires a computer and a Discord account.

# Installation

__*For installation on a Linux (Ubuntu based) servers...*__

- Install necessary base dependencies:
	- Run "sudo bash install.sh"

- Duplicate or rename ".env.example" to ".env" and edit the following properties:
	- TOKEN ( Your bot's Token... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- CLIENT_ID ( Your bot's Client ID... [Tutorial](https://discordjs.guide/preparations/setting-up-a-bot-application.html) )
	- GUILD_ID ( Your server's Guild ID... [Tutorial](https://support.discord.com/hc/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) )

- Finally, create the service files (see unit/readme for more information)...

- Depending on installation/executed permissions, the YT-DLP may not have the correct permissions...
  	- You can use chmod (or similar utilities) to give YT-DLP executable perms

__*For installation on a Windows (10/2019+) servers...*__

- Install [Node.js](https://nodejs.org/en/download) (this will also install [NPM](https://www.npmjs.com/))

- Opening your terminal (command prompt/powershell)
	- Right-click while holding Shift in the Virtuoso folder and select the option to open a terminal, command prompt, or powershell window in that directory

- Install necessary Node dependencies:
	- Run "npm i --production" in the terminal windows
	
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
- After adding your bot to any servers, you must register your slash commands by running "node deploy.js" in the terminal
- Start your bot:
	- On Linux run "sudo service virtuoso start"
	- On Windows open the "Start.bat" script
- Bot status:
	- On Linux run "sudo service virtuoso status"
	- On Windows bring your terminal window to the foreground
- Stop your bot:
	- On Linux run "sudo service virtuoso stop"
	- On Windows close the terminal window
- Discord Commands:
	- /play: Plays the linked (or searched) YouTube audio
	- /skip: Skips the current song
	- /pause: Pauses music playback
	- /resume: Resumes music playback
	- /stop: Disconnects the bot and resets audio state
	- /loop: Toggles looping feature
	- /about: Displays an overview of Virtuoso
	- /ping: Tests your slash command
