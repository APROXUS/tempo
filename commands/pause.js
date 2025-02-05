const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { pause } = require('../controller');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('pause')
        .setDescription('Pauses music playback...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('⏸️  Pausing song...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });

        pause(interaction);
    }
}
