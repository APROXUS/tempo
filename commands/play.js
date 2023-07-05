const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { play, add, queue, last } = require('../controller');
const { promisify } = require('util');

const exec = promisify(require('node:child_process').exec);
const writeFile = promisify(require('node:fs').writeFile);

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

        let upone;
        if (process.platform === 'win32') {
            upone = __dirname.split('\\');
        } else {
            upone = __dirname.split('/');
        }
        upone.pop();

        const music = `${upone.join('/')}/music/${interaction.guildId}/`;

        await interaction.deferReply();

        const query = interaction.options.getString('query').replace(/('|"|\/|\\)/g, '_');

        const command = `./yt-dlp --quiet --print-json --no-playlist --format 'ba' --default-search 'ytsearch' --output '${music}%(id)s.webm' '${query}'`;

        const shell = ((process.platform === 'win32') ? 'powershell.exe' : '/bin/bash');

        let output;
        try {
            const { stdout } = await exec(command, { shell: shell, cwd: __dirname });
            output = stdout;
        } catch {
            const embed = new EmbedBuilder()
                .setTitle('🛑  Could add this song, try another...')
                .setColor(0x8617FE)
            
            await interaction.editReply({
                embeds: [embed]
            });

            return;
        }

        add();

        await writeFile(`${music}${last()}.json`, output);

        const object = JSON.parse(output);

        const embed = new EmbedBuilder()
            .setTitle(`🎵  ${queue() === 0 ? 'Playing' : 'Added'}: ${object.title}`)
            .setDescription(object.uploader)
            .setThumbnail(object.thumbnail)
            .setColor(0x8617FE)
                
        await interaction.editReply({
            embeds: [embed]
        });

        if (queue() === 0) { play(interaction) }
    }
}
