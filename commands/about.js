const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('about')
        .setDescription('Shows details on the KPNC Virtuoso project...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('About Virtuoso:')
            .setDescription('KPNC Technology: Virtuoso is a simple music bot for Discord. It utilizes the popular Discord.js and YT-DLP libraries to play YouTube audio in your Discord server. \r\n \r\n Virtuoso Features: \r\n • /play: Plays the linked (or searched) YouTube audio \r\n • /pause: Pauses music playback \r\n • /resume: Resumes music playback \r\n • /skip: Skips the current song \r\n • /loop: Toggles looping feature \r\n • /stop: Disconnects Virtuoso and resets audio state \r\n \r\n Check out the project at: https://github.com/kpncio/virtuoso')
            .setFooter({ text: 'Please report bugs on GitHub' })
            .setThumbnail('https://content.kpnc.io/img/kpnc/virtuoso.png')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
