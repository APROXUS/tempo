//
// Use PM2 (npm) to run the service in the background...
// Use 'node run tsc' for compiler...
// Use 'nodemon .' for server...
//

// Imports
import DiscordJS, { Intents } from 'discord.js'
import dotenv from 'dotenv'
dotenv.config()

// Variables
const guildid = '779283948059623455'
var songext = '.m4a'
var songcur = ''

// Main Thread
const client = new DiscordJS.Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MESSAGES,
        Intents.FLAGS.GUILD_VOICE_STATES
    ]
})

client.on('ready', () => {
    console.log('(STANDBY) The bot is ready...')

    const guild = client.guilds.cache.get(guildid)
    let commands

    if (guild) {
        commands = guild.commands
    } else {
        commands = client.application?.commands
    }

    commands?.create({
        name: 'ping',
        description: 'Responds with pong...'
    })

    commands?.create({
        name: 'play',
        description: 'Plays the inputted video URL or the first YouTube result...',
        options: [
            {
                name: 'video',
                description: 'The URL or YouTube search to play...',
                required: true,
                type: DiscordJS.Constants.ApplicationCommandOptionTypes.STRING
            }
        ]
    })

    commands?.create({
        name: 'skip',
        description: 'Skips the current music...'
    })

    commands?.create({
        name: 'loop',
        description: 'Enables music looping...'
    })
})

client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) {
        return
    }

    const { commandName, options } = interaction

    if (commandName === 'ping') {
        interaction.reply({
            content: 'pong',
            ephemeral: true
        })
    } else if (commandName === 'play') {
        const video = options.getString('video')!

        // Checking if the message author is in a voice channel.
        if (!interaction.member.voice.channel) return interaction.reply("You must be in a voice channel.");
        // Checking if the bot is in a voice channel.
        if (interaction.guild.me.voice.channel) return interaction.reply("I'm already playing.");
        
        // Joining the channel and creating a VoiceConnection.
        interaction.member.voice.channel.join().then(VoiceConnection => {
            // Playing the music, and, on finish, disconnecting the bot.
            VoiceConnection.play("StillDRE.mp3").on("finish", () => VoiceConnection.disconnect());
        })

        interaction.reply({
            content: `Playing ${video} now...`
        })
    } else if (commandName === 'skip') {
        interaction.reply({
            content: 'Skipping current song...'
        })
    } else if (commandName === 'loop') {
        interaction.reply({
            content: 'Now looping songs...'
        })
    }
})

client.login(process.env.TOKEN)