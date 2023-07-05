const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { loop } = require('../controller');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('loop')
        .setDescription('Toggles looping feature...'),

    async execute(interaction) {
        const looping = loop(true);

        const embed = new EmbedBuilder()
            .setTitle(`🔁  Looping ${looping ? 'enabled' : 'disabled'}...`)
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
