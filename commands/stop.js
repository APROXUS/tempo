const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { stop } = require('../controller');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('stop')
        .setDescription('Disconnects Virtuoso and resets audio state...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('⏹️  Stopping Virtuoso...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });

        stop(interaction);
    }
}
