import discord
import os
import schedule
from dotenv import load_dotenv
project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

client = discord.Client()
meetings = []

async def make_meeting(parameters):
    #Assume only name
    name = parameters[0]
    meetings.append(schedule.Meeting(name))

async def show_meetings(message):
    for meeting in meetings:
        await message.channel.send(meeting.getName())

async def delete_meeting(message):
    for meeting in meetings:
      print(meeting.getName(),"a")
      print(message,"b")
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
