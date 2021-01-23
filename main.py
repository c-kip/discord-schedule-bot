import discord
import os
import schedule
from dotenv import load_dotenv
project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)
client = discord.Client()
meetings = []


async def dm_missing(message):
    author = message.author    
    testing = client.users
    
    if (author.voice is None):
        await message.channel.send('Sorry, you are not currently in a voice channel.')
    else:
        channel = author.voice.channel
        
        for person in participants:
            await message.channel.send(person)
            if person.voice.channel != channel:
                await person.send('why u no in meeting')

            else:
                await person.send('u in meeting :)')
    
    
async def make_meeting(parameters):
    #Assume only name
    name = parameters[0]
    meetings.append(schedule.Meeting(name))

async def show_meetings(message):
    for meeting in meetings:
        await message.channel.send(meeting.getName())
async def delete_meeting(message):
    for meeting in meetings:
      if (meeting.getName() == message[0]):
        meetings.remove(meeting)
          

async def process_command(message):
    parameters = message.content.split(' ')

    if (len(parameters) > 0):
        if (parameters[0] == 'hello'):
            await message.channel.send('Hello!')
        elif (parameters[0] == 'stop'):
            await message.channel.send('Buy-bye!')
            await client.logout()
        elif (parameters[0] == 'meeting'):
            await make_meeting(parameters[1:])
        elif (parameters[0] == 'show_meetings'):
            await show_meetings(message)
        elif (parameters[0] == 'missing'):
            await dm_missing(message)
            # await message.channel.send(message.author)
        elif (parameters[0] == 'delete_meeting'):
            await delete_meeting(parameters[1:])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$'):
        message.content = message.content[1:]
        await process_command(message)
        
client.run(os.getenv('TOKEN'))
