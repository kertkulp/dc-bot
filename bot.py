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

client.run(TOKEN)