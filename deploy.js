const { REST } = require("@discordjs/rest");
const { Routes } = require("discord.js");

require('dotenv').config();
const token = process.env.TOKEN;
const guildId = process.env.GUILD_ID;
const clientId = process.env.CLIENT_ID;

const commandFiles = require('./files').getFiles('./commands');
let commands = [];

for (const file of commandFiles) {
    const command = require(file);

    commands.push(command.data.toJSON());
}

const rest = new REST({ version: '10' }).setToken(token);

// rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commands })
//     .then(() => console.log('Registered application commands!'))

rest.put(Routes.applicationCommands(clientId), { body: commands })
    .then(() => console.log('Registered application commands!'))
