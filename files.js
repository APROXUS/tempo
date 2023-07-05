const { Collection } = require('discord.js');
const { readdirSync } = require('node:fs');

module.exports = {
    getFiles(folder) {
        const files = readdirSync(folder, {
            withFileTypes: true
        });
    
        let commandFiles = [];
    
        for (const file of files) {
            if (file.isDirectory()) {
                commandFiles = [
                    ...commandFiles,
                    ...getFiles(`${folder}/${file.name}`)
                ];
            } else if (file.name.endsWith('.js')) {
                commandFiles.push(`${folder}/${file.name}`);
            }
        }
    
        return commandFiles;
    }, getCommands(folder) {
        const commandFiles = require('./files').getFiles(folder);
        let commands = new Collection;
    
        for (const file of commandFiles) {
            const command = require(file);
        
            commands.set(command.data.toJSON().name, command);
        }
    
        return commands;
    }
}
