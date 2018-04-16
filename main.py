import discord
import os

client = discord.Client()
players = {}

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token


@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print("=================================")
    await client.change_presence(game=discord.Game(name="🎶 +AJUDA", url='https://twitch.tv/TheDiretor', type=1))

@client.event
async def on_message(message):
    if message.content.startswith('+sair'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        try:
            voice_client = client.voice_client_in(message.server)
            await voice_client.disconnect()
            await client.send_message(message.channel, "Estou saindo deste canal! :cd:")
        except AttributeError:
            await client.send_message(message.channel, ":x: Não estou conectado a nenhum canal de voz!")

    if message.content.startswith('+tocar '):
            yt_url = message.content[7:]
            if client.is_voice_connected(message.server):
                    voice = client.voice_client_in(message.server)
                    link = message.content[7:]
                    player = await voice.create_ytdl_player("ytsearch:{}".format(link))
                    players[message.server.id] = player
                    player.start()
                    await client.send_message(message.channel, "Tocando agora: **{}** :cd:".format(player.title))

            if not client.is_voice_connected(message.server):
                try:
                    channel = message.author.voice.voice_channel
                    voice = await client.join_voice_channel(channel)
                    link = message.content[7:]
                    player = await voice.create_ytdl_player("ytsearch:{}".format(link))
                    players[message.server.id] = player
                    player.start()
                    await client.send_message(message.channel, "Tocando agora: **{}** :cd: ".format(player.title))
                except discord.errors.InvalidArgument:
                    await client.send_message(message.channel, ":x: Você não está conectado a nenhum canal de voz!")

    if message.content.startswith('+parar'):
        try:
            canaldevoz = client.voice_client_in(message.server)
            await canaldevoz.disconnect()
            await client.send_message(message.channel, "A música foi parada com sucesso! :cd:")
        except AttributeError:
            await client.send_message(message.channel, ":x: O bot não está reproduzindo músicas ou não está conectado à um canal de voz!")

    if message.content.startswith('+pausar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
            players[message.server.id].pause()
            await client.send_message(message.channel, "A música foi pausada! :cd:")
    if message.content.startswith('+retomar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
            players[message.server.id].resume()
            await client.send_message(message.channel, "A música foi retomada! :cd:")

    if message.content.lower().startswith('+ajuda'):
        embed = discord.Embed(
            title="Meus comandos musicais:",
            color=0xFF5079,
            description="***+tocar*** `<link da música>` » Toco a música solicitada pelo usuário. \n"
                        "***+tocar*** `<nome da música>` » Busco pela música no YouTube. \n"
                        "***+parar*** » Paro de tocar a música e me desconecto do canal. \n"
                        " \n"
                        "***Comandos para admin+:*** \n"
                        "***+pausar*** » Pauso a música. \n"
                        "***+retomar*** » Retorno a música. \n"
                        "***+sair*** » Saio do canal. \n"
                        "***Qualquer dúvida me contate no Twitter!*** [Clique aqui](https://twitter.com/brunoqq_)"
        )
        embed.set_author(
            name="BRN Music 🎵",
            icon_url=client.user.avatar_url,
            url="https://twitter.com/brunoqq_"
        )
        embed.set_footer(
            text="Copyright © 2018 Bruno",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei todos os meus comandos __musicais__ no seu privado!".format(
            message.author.mention))
        await client.send_message(message.author, embed=embed)

client.run(token)
