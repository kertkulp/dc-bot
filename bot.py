import discord
import asyncio
import youtube_dl
from discord.ext import commands
import config as cfg
from datetime import datetime
import math
from lists import *

TOKEN = cfg.token

client = commands.Bot(command_prefix = '!')
server = discord.Server(id='480289155138584576')

authors = []
messages = []
warned_users = []
banned_users =[]

players = {}
queues ={}
first_time_player = True

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

@client.event
async def on_member_join(member):
    channel = discord.Object(id='480289155138584578') # enable developer mode to check id
    msg = 'Welcome to the server {0}!'.format(member.mention)
    role = discord.Object('482188344256757770') # \@rolename to check role id
    await client.send_message(channel, msg)
    await client.add_roles(member, role)

@client.event
async def on_member_remove(member):
    channel = discord.Object(id='480289155138584578')
    msg = '{0} has left the server!'.format(member.mention)
    await client.send_message(channel, msg)

@client.event
async def on_message(message):
    #############Spam Filter
    channel = discord.Object(id='480289155138584578')
    warning_message = '{0} stop spamming or you will be banned!'.format(message.author.mention)
    if message.author == client.user:
        return

    if message.author.id != client.user.id:
        t = datetime.now().time()
        time_now =  (t.hour * 60 + t.minute) * 60 + t.second
        print(time_now)
     
        authors.append(
            [
                time_now,
                message.author.id
            ]
        )
        messages.append(
            [
                message.content,
                message.author.id
            ]
        )
        #print(authors)
        #print(messages)
        
        matched_messages = 0

        for i in messages:
            print("see on i0", i[0])
            print("see on message.content", message.content)
            print("see on i1", i[1])
            print("see on message.author.id", message.author.id)
            print("see on client.user.id", client.user.id)
            if (i[0] == message.content) and (i[1] == message.author.id) and (message.author.id != client.user.id):
                matched_messages += 1
        
        print(matched_messages)

        if(matched_messages == 5) and (message.author.id not in warned_users):
            warned_users.append(message.author.id)
            await client.send_message(channel, warning_message)
        
        if(matched_messages == 10) and (message.author.id not in banned_users):
            await client.ban(message.author, 1)
            print('test1')

        time_match = 0
        
        for index, i in enumerate(authors):
            if(i[0] > time_now - 20):
                time_match += 1
                if(time_match == 3) and (message.author.id not in warned_users):
                    warned_users.append(message.author.id)
                    await client.send_message(channel, warning_message)
                elif(time_match == 5):
                    if(message.author.id not in banned_users):
                        await client.ban(message.author, 1)
                        print('test2')
            elif(i[0] < time_now - 20):
                try:
                    del i
                    del warned_users[index]
                    del banned_users[index]
                except Exception:
                    pass
            if(len(messages) >= 200):
                messages.pop([0])     
    #############Sound/pic commands
    if str(message.content) in str(f_pic_name_list()):
        msg = (str(message.content)).format(message)
        await client.send_file(message.channel, "pics/"+str(message.content)[1:]+".jpg")
    if str(message.content) in str(f_sound_name_list()):
        voice_channel = message.author.voice_channel
        if voice_channel is not None:
            voice = await client.join_voice_channel(voice_channel)
            try:
                player = voice.create_ffmpeg_player("audio/"+str(message.content)[1:]+".wav")
                player.start()
                while player.is_playing():
                    pass
                await voice.disconnect()
            except discord.ClientException:
                await voice.disconnect()

    if message.content.startswith('!help'):
        embed = discord.Embed(title="Sem-bot", description="Bot is here to entertain you", color=0x00ff00)
        embed.add_field(name="!pics", value="Displays all the picture commands", inline=False)
        embed.add_field(name="!audio", value="Displays all the audio commands", inline=False)
        embed.add_field(name="!player", value="Displays all the media player commands", inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!player'):
        embed = discord.Embed(title="Youtube player", description="Make sure you're in a voice channel!", color=0xFF00C1)
        embed.add_field(name="!play [url]", value="Audio from your video will start playing", inline=False)
        embed.add_field(name="!stop", value="Stops the current song", inline=False)
        embed.add_field(name="!pause", value="Pauses the current song", inline=False)
        embed.add_field(name="!resume", value="Continues the current song", inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!pics'):
        msg = (("All the picture commands are: "+", ".join(f_pic_name_list())).format(message))
        await client.send_message(message.channel, msg)

    if message.content.startswith('!sounds'):
        msg = (("All the sound commands are: "+", ".join(f_sound_name_list())).format(message))
        await client.send_message(message.channel, msg)
    

    await client.process_commands(message) #magic line to make commands work after on_message
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