const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('about')
        .setDescription('Shows details on the KPNC Conducter project...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('About Conducter:')
            .setDescription('KPNC Technology: Conducter: is a simple Discord music bot that utilizes the popular Discord.js and Youtube-DL projects. Installing your own version of Conducter is easy and only requires that you have an computer and a Discord account. \r\n \r\n Conducter Features: \r\n • /play: Plays the linked (or searched) YouTube audio \r\n • /pause: Pauses music playback \r\n • /resume: Resumes music playback \r\n • /skip: Skips the current song \r\n • /stop: Disconnects Conducter and resets audio state \r\n \r\n Check out the project at: https://github.com/kpncio/conducter')
            .setThumbnail('https://content.kpnc.io/img/kpnc/conducter.png')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
