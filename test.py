import discord
import asyncio
import youtube_dl
from discord.ext import commands
import config as cfg

TOKEN = cfg.token

client = commands.Bot(command_prefix = '!')
players = {}
queues ={}


async def check_queue(id):
    
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start
    else:
        del players[id]

@client.event
async def on_ready():
    print('Bot running!')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="test"))
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server

    if client.is_voice_connected(server):
        print('')
    else:
        await client.join_voice_channel(channel)

    voice_client = client.voice_client_in(server)

    if server.id not in players:
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()

    else:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await client.say('We have added your song to the queue!')

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id

    if players[id] != []:
        players[id].stop()
        del players[id]
    else:
        players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

    
client.run(TOKEN)