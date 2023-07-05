const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { resume } = require('../controller');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('resume')
        .setDescription('Resumes music playback...'),

    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('▶️  Resuming song...')
            .setColor(0x8617FE)

        await interaction.reply({
            embeds: [embed]
        });

        resume(interaction);
    }
}
