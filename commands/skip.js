const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { next } = require('../controller');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('skip')
        .setDescription('Skips the current song...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('⏭️  Skipping song...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });

        next(interaction);
    }
}
