import discord
import os
import schedule
import datetime
from dotenv import load_dotenv
project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

client = discord.Client()
meetings = []

async def make_meeting(parameters):
    #Name parameter
    name = parameters[0]

    #Time parameter HH:MM (24HR)
    meeting_time = datetime.datetime.now().time #Default is now
    if (len(parameters[1]) == 5):
        meeting_time = datetime.time(int(parameters[1][:2]), int(parameters[1][3:]))

    #Date parameter DD/MM/YYYY (if year is omitted, assumed the current)
    meeting_date = datetime.date.today() #If the date is omitted, assume today
    if (len(parameters[2]) == 5):
        meeting_date = datetime.date(meeting_date.year, int(parameters[2][3:]), int(parameters[2][:2]))
    elif (len(parameters[2]) == 10):
        meeting_date = datetime.date(int(parameters[2][6:]), int(parameters[2][3:5]), int(parameters[2][:2]))

    #Participants parameter - all the @ users
    #TODO

    #Desc parameter - string (in quotes)
    #TODO

    #Autoremind parameter - TRUE or FALSE
    #TODO

    meetings.append(schedule.Meeting(name, meeting_time, meeting_date))

async def show_meetings(message):
    for meeting in meetings:
        await message.channel.send(meeting.getName() + "\n" + 
              str(meeting.getTime().hour).zfill(2) + ":" + str(meeting.getTime().minute).zfill(2) + " " + str(meeting.getDate().day).zfill(2) + 
              "/" + str(meeting.getDate().month).zfill(2) + "/" + str(meeting.getDate().year).zfill(2))

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
