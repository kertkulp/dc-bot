import discord
import asyncio
from discord.ext import commands
import config as cfg
from datetime import datetime
import math

TOKEN = cfg.token

client = commands.Bot(command_prefix = '!')
server = discord.Server(id='480289155138584576')

authors = []
messages = []
warned_users = []
banned_users =[]

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

'''def ban(message, userid):
    for i in messages:
        if(i[1] == message.author.id):
            del i
    
    banned_users.append(message.author.id)
   
    ban(Server.get_member(message.author.id), delete_message_days=1)
   
'''
    

    


client.run(TOKEN)