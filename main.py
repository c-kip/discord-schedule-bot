import discord
from discord import DMChannel
import os
import schedule
import datetime
from dotenv import load_dotenv
project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

client = discord.Client()
meetings = []
users = {}


def addUser(user):
    if (user.id not in users.keys()):
        users[user.id] = []

def addUserMeeting(user, meeting):
    addUser(user)
    if (meeting.getName() not in users[user.id]):
        users[user.id].append(meeting.getName())

def removeUserMeeting(user, meeting):
    if (meeting.getName() in users[user]):
        users[user].remove(meeting.getName())
    print(str(users))

async def dm_missing(message):
    author = message.author    
    testing = client.users
    
    if (author.voice is None):
        await message.channel.send('Sorry, you are not currently in a voice channel.')
    else:
        channel = author.voice.channel
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M')
        current_date = now.strftime('%B %d, %Y')

        # checking to see which meeting is happening now
        for meeting in meetings:
            print (meeting.getDateTime())
            print (datetime.datetime.now())
            print (meeting.getEndDateTime())
            if datetime.datetime.now() >= meeting.getDateTime() and datetime.datetime.now() <= meeting.getEndDateTime():
                if not(admin_authentication(author, meeting)):
                    await message.channel.send("{} could not ping everyone missing for the meeting {}".format(await client.guilds[0].fetch_member(author.id), meeting.getName()))
                    return
                missing = meeting
                await message.channel.send(meeting.getName() + ' is taking place right now')
                for person in missing.getParticipants():
                    if person.voice is None or person.voice.channel != channel:
                        await person.send('why u no in meeting :( ')

                    else:
                        await person.send('u in meeting :)')
                await message.channel.send("{} pinged everyone missing for the meeting {}".format(await client.guilds[0].fetch_member(author.id), meeting.getName()))
                return
        
async def helpCommands (message):
    embed_help = discord.Embed(title="Help Center:", color=0x685BC7) 
    msg = """Welcome to ___ bot! \nHere are some of the commands you can use: 
    \n ```$meeting - allows you to schedule a new meeting 
    \n you can mix and match these parameters but make sure you have the title!
    \n parameters: 
    \n title: **all meetings must have this** (e.g. $meeting party)
    \n start time: 24h-time, defaults to current time (e.g. $meeting party 13:35)
    \n duration: defaults to 1 hour (e.g. $meeting party 13:35 1:45)
    \n date: defaults to current date (e.g. $meeting party 24/01/2021)
    \n participants: @ any users you want to schedule for the meeting (e.g. $meeting party @joe)
    \n description: put your meeting description in between ' ' (e.g. $meeting party 'susan's birthday!')
    \n auto remind: use TRUE or FALSE to turn auto remind on or off, defaults to FALSE (e.g. $meeting party TRUE)```
    ```$show_meetings - will show all currently scheduled meetings```
    ```$edit - lets meeting organizers and administrators edit meeting details```
    ```$missing - checks the sender's voice channel to see if all meeting attendees are present and sends a direct message to those who are missing```
    ```$delete_meeting - deletes a meeting given its name```
    ```$my_meetings - sends you a direct message of all of your scheduled meetings```
    ```$add_admin - adds an administrator to the meeting given the meeting name and the @ of the new administrator (e.g. $add_admin party @bob)```
    ```$remove_admin - adds an administrator to the meeting given the meeting name and the @ of the new administrator (e.g. $remove_admin party @bob)```
    """
    embed_help.description = msg
    await message.channel.send (embed=embed_help)


    
async def parse_meeting_info(parameters):
    meeting_time = None
    meeting_date = None
    meeting_duration = None
    start_recorded = False
    participants = []
    desc = ''
    auto_remind = None
    copy_desc = False

    #Loop through the remaining parameters
    for param in parameters:

        #Time parameter HH:MM (24HR)
        if (len(param) >= 3 and param[2] == ':'):
            #The first time found is assumed to be the start time
            if (not(start_recorded)):
                minutes = 0 #Default the minutes to 0 if not provided
                try:
                    minutes = int(param[3:])
                except:
                    minutes = 0
                meeting_time = datetime.time(int(param[:2]), minutes)
                start_recorded = True
            #The second time found is assumed to be the duration
            else:
                minutes = 0 #Default the minutes to 0 if not provided
                try:
                    minutes = int(param[3:])
                except:
                    minutes = 0
                meeting_duration = datetime.timedelta(hours=int(param[:2]), minutes=minutes)

        #Time parameter alternate format H:MM (24HR)
        if (len(param) >= 2 and param[1] == ':'):
            #The first time found is assumed to be the start time
            if (not(start_recorded)):
                minutes = 0 #Default the minutes to 0 if not provided
                try:
                    minutes = int(param[2:])
                except:
                    minutes = 0
                meeting_time = datetime.time(int(param[:1]), minutes)
                start_recorded = True
            #The second time found is assumed to be the duration
            else:
                minutes = 0 #Default the minutes to 0 if not provided
                try:
                    minutes = int(param[2:])
                except:
                    minutes = 0
                meeting_duration = datetime.timedelta(hours=int(param[:1]), minutes=minutes)

        #Date parameter DD/MM/YYYY (if year is omitted, assumed the current)
        if (len(param) == 5 and param[2] == '/'):
            meeting_date = datetime.date(datetime.datetime.now().year, int(param[3:]), int(param[:2]))
        elif (len(param) == 10 and param[2] == '/' and param[5] == '/'):
            meeting_date = datetime.date(int(param[6:]), int(param[3:5]), int(param[:2]))

        #Participants parameter - all the @ users
        if (param[:3] == '<@!'):
            participants.append(await client.guilds[0].fetch_member(int(param[3:-1]))) #Add the user as a 'member' object

        #Desc parameter start - string (in quotes)
        if (param.startswith("'")):
            copy_desc = True
            param = param[1:] #Remove the quotation
            desc = ""
        
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
        elif (param.lower() == 'false'):
            auto_remind = False
    
    return meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind

async def make_meeting(parameters):
    #Name parameter
    name = "Undefined"
    if (len(parameters) >= 1):
        for meet in meetings:
            if (meet.getName() == parameters[0]):
                return "A meeting already uses that name!"
        name = parameters[0]
    else:
        return "No parameters given!"

    meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind = await parse_meeting_info(parameters[1:])

    if (meeting_time == None):
        meeting_time = datetime.datetime.now().time() #Default time is now
    if (meeting_duration == None):
        meeting_duration = datetime.timedelta(hours=1) #Default is one hour long
    if (meeting_date == None):
        meeting_date = datetime.date.today() #If the date is omitted, assume today
    if (auto_remind == None):
        auto_remind = False #Default is no auto_remind

    meetings.append(schedule.Meeting(name, meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind))
    
    for user in participants:
        addUserMeeting(user, meetings[-1])

    return None

#Updates the parameters for the given meetings
async def update_meeting(message, parameters):

    for meeting in meetings:
        if (meeting.getName() == parameters[0]):
            if not (admin_authentication(message.author, meeting)):
                return False

    found = -1
    for i in range(len(meetings)):
        if (meetings[i].getName() == parameters[0]):
            found = i
    
    if (found == -1):
        await message.channel.send("No meeting of name '{}' found.".format(parameters[0]))
        return False

    meeting_time, meeting_duration, meeting_date, participants, desc, auto_remind = await parse_meeting_info(parameters[1:])

    #Set any changed values
    if (meeting_time != None):
        meetings[found].setTime(meeting_time)
    if (meeting_duration != None):
        meetings[found].setDuration(meeting_duration)
    if (meeting_date != None):
        meetings[found].setDate(meeting_date)
    if (participants != []): #Not NONE
        for person in participants:
            if (not(meetings[found].addParticipant(person))):
                try:
                    await message.channel.send("{} has already signed up for {}".format(person, meetings[found].getName()))
                except:
                    print("Error, likelyl no message given (meeting creation issue).")
    if (desc != ''):
        meetings[found].setDesc(desc)
    if (auto_remind != None):
        meetings[found].setAutoRemind(auto_remind)

    return True

async def show_meetings(message):
    if (len(meetings) == 0):
        await message.channel.send("No meetings scheduled")
    for meeting in meetings:
        await message.channel.send(embed=meeting.getEmbed())

async def delete_meeting(message, author):
    for meeting in meetings:
      if (meeting.getName() == message):
        if not (admin_authentication(author, meeting)):
            return False
        meetings.remove(meeting)
        for user in users.keys():
            removeUserMeeting(user, meeting)
        return True
    return False

async def my_meetings(message):
    user_meetings = []
    user = await client.fetch_user(message.author.id)

    if (len(meetings) == 0):
        for meeting in meetings:
            participants = meeting.getParticipants()
        if message.author in participants:
            user_meetings.append(meeting)

        await DMChannel.send(user, "Upcoming Meetings:")
        for meeting in user_meetings:
            await DMChannel.send(user, embed=meeting.getEmbed())
    else:
        await DMChannel.send(user, "No upcoming meetings")
        
def admin_authentication(user, meeting):
    flag = False
    for admin in meeting.getAdmin():
        if (user.id == admin.id):
            flag = True
    return flag

async def process_command(message):
    parameters = message.content.split(' ')

    if (len(parameters) > 0):
        if (parameters[0] == 'hello'):
            await message.channel.send("Hello!")
        elif (parameters[0] == 'stop'):
            await message.channel.send('Buy-bye!')
            await client.logout()
        elif (parameters[0] == 'meeting'):
            error = await make_meeting(parameters[1:])
            if (error != None):
                await message.channel.send(error)
            else:
                meetings[-1].addAdmin(await client.guilds[0].fetch_member(message.author.id))
                await show_meetings(message)
                message = await message.channel.send('React with \N{THUMBS UP SIGN} to enroll in the meeting {}'.format(parameters[1]))
                await message.add_reaction('\N{THUMBS UP SIGN}')
                meetings[-1].setMessage(message)
        elif (parameters[0] == 'show_meetings'):
            await show_meetings(message)
        elif (parameters[0] == 'edit'):
            flag = await update_meeting(message, parameters[1:])
            if flag:
                await message.channel.send('The meeting {} was successfully edited by {}'.format(parameters[1], await client.guilds[0].fetch_member(message.author.id)))
            else:
                await message.channel.send('The meeting {} could not be edited by {}'.format(parameters[1], await client.guilds[0].fetch_member(message.author.id)))
        elif (parameters[0] == 'missing'):
            await dm_missing(message)
            # await message.channel.send(message.author)
        elif (parameters[0] == 'delete_meeting'):
            flag = await delete_meeting(parameters[1], message.author)
            if flag:
                await message.channel.send('The meeting "{}" has been successfully deleted by {}'.format(parameters[1], await client.guilds[0].fetch_member(message.author.id)))
            else:
                await message.channel.send('The meeting "{}" could not be deleted deleted by {}'.format(parameters[1], await client.guilds[0].fetch_member(message.author.id)))
        elif (parameters[0] == 'my_meetings'):
            await my_meetings(message)
        elif (parameters[0] == 'help'):
            await helpCommands(message)
        elif (parameters[0] == 'add_admin'):
            flag = False
            for meeting in meetings:
                if (meeting.getName() == parameters[1] and admin_authentication(message.author, meeting)):
                    flag = meeting.addAdmin(await client.guilds[0].fetch_member(int(parameters[2][3:-1])))
            if flag:
                await message.channel.send('{} was successfully made an admin for the meeting {} by {}'.format(await client.guilds[0].fetch_member(int(parameters[2][3:-1])), parameters[1], await client.guilds[0].fetch_member(message.author.id)))
            else:
                await message.channel.send('{} could not be made an admin for the meeting {} by {}'.format(await client.guilds[0].fetch_member(int(parameters[2][3:-1])), parameters[1], await client.guilds[0].fetch_member(message.author.id)))
        elif (parameters[0] == 'remove_admin'):
            flag = False
            for meeting in meetings:
                if (meeting.getName() == parameters[1] and admin_authentication(message.author, meeting)):
                    flag = meeting.removeAdmin(await client.guilds[0].fetch_member(int(parameters[2][3:-1])))
            if flag:
                await message.channel.send('{} was demoted from admin by {} for the meeting {}'.format(await client.guilds[0].fetch_member(int(parameters[2][3:-1])), await client.guilds[0].fetch_member(message.author.id), parameters[1]))
            else:
                await message.channel.send('{} could not be demoted from admin by {} for the meeting {}'.format(await client.guilds[0].fetch_member(int(parameters[2][3:-1])), await client.guilds[0].fetch_member(message.author.id), parameters[1]))
        elif (parameters[0] == 'leave_meeting'):
            flag = False
            for meeting in meetings:
                if (meeting.getName() == parameters[1]):
                    flag = meeting.removeParticipant(await client.guilds[0].fetch_member(message.author.id))
            if flag:
                await message.channel.send('{} was successfully removed from the meeting {}'.format(await client.guilds[0].fetch_member(message.author.id), parameters[1]))
            else:
                await message.channel.send('{} could not be removed from the meeting {}'.format(await client.guilds[0].fetch_member(message.author.id), parameters[1]))

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if(user != client.user and reaction.emoji == '\N{THUMBS UP SIGN}'):
        for meeting in meetings:
            if (reaction.message == meeting.getMessage()):
                if (meeting.addParticipant(user)):
                    addUserMeeting(user, meeting)
                    await channel.send("{} has successfully signed up for {}".format(user.name, meeting.name))
                else:
                    await channel.send("{} has already signed up for {}".format(user.name, meeting.name))

@client.event 
async def on_guild_join (guild):
    embed_greeting = discord.Embed(title="Hello!", color=0x685BC7) 
    msg = "Hi, thanks for inviting me! \n- my prefix is `$` \n- you can see a list of commands by typing `$help`"
    embed_greeting.description = msg
    
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send (embed=embed_greeting)
        break

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
