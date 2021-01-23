import discord
import os
import schedule
import datetime
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
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        current_date = now.strftime('%B %d, %Y')

        for meeting in meetings:
            if meeting.getDate == current_date:
                if meeting.getTime == current_time:
                    print ("todayy is meeting")

        print('current time = ', current_time)
        # for person in participants:
        #     await message.channel.send(person)
        #     if person.voice.channel != channel:
        #         await person.send('why u no in meeting :( ')

        #     else:
        #         await person.send('u in meeting :)')
    
    
async def make_meeting(parameters):
    #Name parameter
    name = "Undefined"
    if (len(parameters) >= 1):
        name = parameters[0]

    #Default values
    meeting_time = datetime.datetime.now().time() #Default time is now
    meeting_date = datetime.date.today() #If the date is omitted, assume today
    participants = []
    desc = ""
    copy_desc = False
    auto_remind = False #Default is no auto_remind

    #Loop through the remaining parameters
    for param in parameters[1:]:
        print(param)

        #Time parameter HH:MM (24HR)
        if (len(param) == 5 and param[2] == ':'):
            meeting_time = datetime.time(int(param[:2]), int(param[3:]))

        #Date parameter DD/MM/YYYY (if year is omitted, assumed the current)
        if (len(param) == 5 and param[2] == '/'):
            meeting_date = datetime.date(meeting_date.year, int(param[3:]), int(param[:2]))
        elif (len(param) == 10 and param[2] == '/' and param[5] == '/'):
            meeting_date = datetime.date(int(param[6:]), int(param[3:5]), int(param[:2]))

        #Participants parameter - all the @ users
        if (param[:3] == '<@!'):
            participants.append(await client.guilds[0].fetch_member(int(param[3:-1]))) #Add the user as a 'member' object

        #Desc parameter start - string (in quotes)
        if (param.startswith("'")):
            copy_desc = True
            param = param[1:] #Remove the quotation
        
        #End of desc
        if (param[-1] == "'"):
            copy_desc = False
            desc += param[:-1] #Remove the quotation

        #Add part of the desc
        if (copy_desc):
            desc += param + ' '

        #Autoremind parameter - TRUE or FALSE
        if (param.lower() == "true"):
            auto_remind = True

    meetings.append(schedule.Meeting(name, meeting_time, meeting_date, participants, desc, auto_remind))

async def show_meetings(message):
    for meeting in meetings:
        participant_names = ""
        for participant in meeting.getParticipants():
            participant_names += participant.display_name + ", "
        await message.channel.send(meeting.getName() + "\n" + 
              str(meeting.getTime().hour).zfill(2) + ":" + str(meeting.getTime().minute).zfill(2) + " " + str(meeting.getDate().day).zfill(2) + 
              "/" + str(meeting.getDate().month).zfill(2) + "/" + str(meeting.getDate().year).zfill(2) + "\n" +
              "Participants: " + participant_names + "\n" + 
              "Desc: " + meeting.getDesc() + "\n" +
              "Auto-Remind: " + str(meeting.getAutoRemind()))

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
            message = await message.channel.send('React with \N{THUMBS UP SIGN} to enrol in {}'.format(parameters[1]))
            await message.add_reaction('\N{THUMBS UP SIGN}')
            meetings[-1].setMessage(message)
        elif (parameters[0] == 'show_meetings'):
            await show_meetings(message)
        elif (parameters[0] == 'check_meetings'):
            for meeting in meetings:
                await message.channel.send(meeting)
        elif (parameters[0] == 'missing'):
            await dm_missing(message)
            # await message.channel.send(message.author)
        elif (parameters[0] == 'delete_meeting'):
            await delete_meeting(parameters[1:])

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if(user != client.user and reaction.emoji == '\N{THUMBS UP SIGN}'):
        for meeting in meetings:
            if (reaction.message == meeting.getMessage()):
                meeting.addParticipant(user)
                await channel.send("{} has added successfully signed up for {}".format(user.name, meeting.name))

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
