const { joinVoiceChannel, createAudioPlayer, createAudioResource, StreamType } = require('@discordjs/voice');
const { createReadStream } = require('node:fs');

module.exports = {
    async play (interaction, number) {
        const connection = joinVoiceChannel({
            channelId: interaction.member.voice.channel.id,
            guildId: interaction.guild.id,
            adapterCreator: interaction.guild.voiceAdapterCreator
        });

        const player = createAudioPlayer();

        const subscription = connection.subscribe(player);

        const resource = createAudioResource(createReadStream(`music/${interaction.guildId}/${number}.webm`), {
            inputType: StreamType.WebmOpus
        });

        player.play(resource);
    }
}