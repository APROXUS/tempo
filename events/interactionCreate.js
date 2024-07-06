const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.commands = require('../files').getCommands('./commands')

module.exports = {
    name: 'interactionCreate',
    async execute(interaction) {
        if(!interaction.isChatInputCommand()) return;

        let command = client.commands.get(interaction.commandName);

        try {
            if (interaction.replied) return;

            command.execute(interaction);
        } catch (error) {
            console.error(error);
        }

        let argument = 'null';
        if (interaction.commandName === 'play') argument = interaction.options.getString('query').replace(/;|:/g, '_');

        console.log(`Command: ${interaction.commandName}; Query: ${argument}; User: ${interaction.user.tag};`);
    }
}
