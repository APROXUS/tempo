const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { play } = require('../controller');
const { promisify } = require('util');

const exec = promisify(require('node:child_process').exec);
const readFile = promisify(require('node:fs').readFile);
const readdir = promisify(require('node:fs').readdir);
const exists = promisify(require('node:fs').exists);

module.exports = {
    data: new SlashCommandBuilder()
        .setName('play')
        .setDescription('Plays YouTube audio depending on the specified link or search query...')
        .addStringOption(option =>
            option
                .setName('query')
                .setDescription('The YouTube link or search query...')
                .setRequired(true)
        ),

    async execute(interaction) {
        if (!interaction.member.voice.channel) {
            const embed = new EmbedBuilder()
            .setTitle('🛑  Please connect to a voice channel...')
            .setColor(0x8617FE)

            await interaction.reply({
                embeds: [embed]
            });

            return;
        }

        await interaction.deferReply();

        const query = interaction.options.getString('query');

        let upone;
        if (process.platform === 'win32') {
            upone = __dirname.split('\\');
        } else {
            upone = __dirname.split('/');
        }
        upone.pop();

        const music = `${upone.join('/')}/music/${interaction.guildId}/`;
        
        let number = 0;

        if (await exists(music)) {
            const files = await readdir(music, {
                withFileTypes: true
            });

            if (files) {
                let order = [];
                for (const file of files) {
                    let name = file.name;
                    order.push(parseInt(name.split('.')[0]));
                }
                order = [...new Set(order)]
        
                number = parseInt(order.reduce((a, b) => Math.max(a, b), -Infinity)) + 1;
            }
        }

        const command = `./yt-dlp --quiet --print-json --no-playlist --format 'ba' --default-search 'ytsearch' --output '${music}${number}.webm' '${query}'`;

        const shell = ((process.platform === 'win32') ? 'powershell.exe' : '/bin/bash');

        const { stdout } = await exec(command, { shell: shell, cwd: __dirname })

        const object = JSON.parse(stdout);

        const embed = new EmbedBuilder()
            .setTitle('🎵  Added: ' + object.title)
            .setDescription(object.uploader)
            .setThumbnail(object.thumbnail)
            .setColor(0x8617FE)

        await interaction.editReply({
            embeds: [embed]
        });

        play(interaction, number);
    }
}
