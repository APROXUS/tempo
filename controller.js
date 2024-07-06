const { joinVoiceChannel, createAudioPlayer, createAudioResource, entersState, VoiceConnectionStatus, AudioPlayerStatus, StreamType } = require('@discordjs/voice');
const { createReadStream } = require('node:fs');
const { EmbedBuilder } = require('discord.js');
const { promisify } = require('util');

const readFile = promisify(require('node:fs').readFile);
const readdir = promisify(require('node:fs').readdir);
const unlink = promisify(require('node:fs').unlink);

let subscription;
let connection;
let resource;
let player;

let queue = 0;
let last = 0;

let loop = false;

module.exports = {
    async play (interaction) {
        queue++;

        connection = joinVoiceChannel({
            channelId: interaction.member.voice.channel.id,
            guildId: interaction.guild.id,
            adapterCreator: interaction.guild.voiceAdapterCreator
        });

        player = createAudioPlayer();

        player.unpause();

        subscription = connection.subscribe(player);

        const object = JSON.parse(await readFile(`music/${interaction.guildId}/${queue}.json`));
        resource = createAudioResource(createReadStream(`music/${interaction.guildId}/${object.id}.webm`), {
            inputType: StreamType.WebmOpus
        });

        player.play(resource);

        player.on(AudioPlayerStatus.Idle, async () => {
            if (!loop) {
                require('./controller').next(interaction);
            } else {
                resource = createAudioResource(createReadStream(`music/${interaction.guildId}/${object.id}.webm`), {
                    inputType: StreamType.WebmOpus
                });

                player.play(resource);
            }
        });

        player.on('error', async () => {
            const embed = new EmbedBuilder()
                .setTitle('🛑  Could not play this song — skipping...')
                .setColor(0x8617FE)
            
            await interaction.channel.send({
                embeds: [embed]
            });

            require('./controller').next(interaction);
        });

        connection.on(VoiceConnectionStatus.Disconnected, async (oldState, newState) => {
            try {
                await Promise.race([
                    entersState(connection, VoiceConnectionStatus.Signalling, 2_000),
                    entersState(connection, VoiceConnectionStatus.Connecting, 2_000),
                ]);
            } catch (error) {
                const embed = new EmbedBuilder()
                    .setTitle('🛑  Please use "/stop" to disconnect Virtuoso...')
                    .setColor(0x8617FE)
                
                await interaction.channel.send({
                    embeds: [embed]
                });

                require('./controller').stop(interaction);
            }
        });
    },
    async next(interaction) {
        if (queue === last) {
            const embed = new EmbedBuilder()
                .setTitle('✅  Queue completed...')
                .setColor(0x8617FE)

            await interaction.channel.send({
                embeds: [embed]
            });

            require('./controller').stop(interaction);
        } else {
            queue++;

            const object = JSON.parse(await readFile(`music/${interaction.guildId}/${queue}.json`));

            const embed = new EmbedBuilder()
                .setTitle(`🎵  Playing: ${object.title}`)
                .setDescription(object.uploader)
                .setThumbnail(object.thumbnail)
                .setColor(0x8617FE)

            await interaction.channel.send({
                embeds: [embed]
            });

            resource = createAudioResource(createReadStream(`music/${interaction.guildId}/${object.id}.webm`), {
                inputType: StreamType.WebmOpus
            });

            player.play(resource);
        }
    },
    async stop(interaction) {
        try {
            subscription.unsubscribe();
            player.stop();
            connection.destroy();
        } catch {
            const embed = new EmbedBuilder()
                .setTitle('🛑  Virtuoso is not connected...')
                .setColor(0x8617FE)
                
            await interaction.editReply({
                embeds: [embed]
            });
        }

        queue = 0;
        last = 0;

        try {
            const files = await readdir('music/' + interaction.guildId, {
                withFileTypes: true
            });
    
            for (const file of files) {
                if (file.name.endsWith('.json')) {
                    await unlink(`${'music/' + interaction.guildId}/${file.name}`);
                }
            }
        } catch {
            const embed = new EmbedBuilder()
                .setTitle('🛑  File error, please reset...')
                .setColor(0x8617FE)
                
            await interaction.channel.send({
                embeds: [embed]
            });
        }
    },
    async pause(interaction) {
        try {
            player.pause();
        } catch {
            const embed = new EmbedBuilder()
                .setTitle('🛑  Virtuoso is not connected...')
                .setColor(0x8617FE)
                
            await interaction.editReply({
                embeds: [embed]
            });
        }
    },
    async resume(interaction) {
        try {
            player.unpause();
        } catch {
            const embed = new EmbedBuilder()
                .setTitle('🛑  Virtuoso is not connected...')
                .setColor(0x8617FE)
                
            await interaction.editReply({
                embeds: [embed]
            });
        }
    },
    add() {
        last++;
    },
    queue() {
        return queue;
    },
    last() {
        return last;
    },
    loop(toggle = false) {
        if (toggle) { loop = !loop; }

        return loop;
    }
}