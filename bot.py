import discord
import asyncio
from discord.ext import commands

TOKEN = 'NDkzNzkzODU2MDczMTA1NDA5.DoqJLg.K1HBokXEM-PYAy185GDLdMgjiJE'

client = commands.Bot(command_prefix = '!')

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


client.run(TOKEN)