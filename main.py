import discord
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

client = discord.Client()

async def process_command(message):
    parameters = message.content.split(' ')

    if (len(parameters) > 0):
        if (parameters[0] == '$hello'):
            await message.channel.send('Hello!')
        elif (parameters[0] == '$stop'):
            await message.channel.send('Buy-bye!')
            await client.logout()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$'):
        await process_command(message)
        
client.run(os.getenv('TOKEN'))