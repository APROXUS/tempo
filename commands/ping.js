const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Returns "Pong!"...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('🏓  Pong!')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
