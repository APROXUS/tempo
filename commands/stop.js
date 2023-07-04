const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('stop')
        .setDescription('Disconnects Conducter and resets audio state...'),

    async execute(interaction) {
        // Stop audio, leave channel, delete guild file

        const embed = new EmbedBuilder()
            .setTitle('⏹️  Stopping Conducter...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
