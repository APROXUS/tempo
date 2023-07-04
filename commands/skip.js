const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('skip')
        .setDescription('Skips the current song...'),

    async execute(interaction) {
        // Start next song, delete last song

        const embed = new EmbedBuilder()
            .setTitle('⏭️  Skipping song...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });
    }
}
