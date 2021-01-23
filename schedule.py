"""
Object template for schedules. Currently
pretty basic and lacking in details (especially
in how participants will be stored).
"""
import datetime
import discord

class Meeting:
    def __init__(self, name, time = datetime.time(0,0,0), date = datetime.date(2000, 1, 1), participants = [], desc = "", auto_remind = False):
        self.name = name
        self.time = time
        self.date = date
        self.participants = participants
        self.desc = desc
        self.auto_remind = auto_remind
        self.message = ""
    
    def getName(self):
        return self.name

    def setTime(self, time):
        self.time = time
    
    def getTime(self):
        return self.time
    
    def setDate(self, date):
        self.date = date
    
    def getDate(self):
        return self.date

    def setDesc(self, desc):
        self.desc = desc
    
    def getDesc(self):
        return self.desc

    def setMessage(self, message):
        self.message = message

    def getMessage(self):
        return self.message

    def setAutoRemind(self, auto_remind):
        self.auto_remind = auto_remind

    def getAutoRemind(self):
        return self.auto_remind

    def addParticipant(self, user):
        #Only add if they haven't been already
        if (not(user in self.participants)):
            self.participants.append(user)
            return True
        return False
    
    def removeParticipant(self, user):
        self.participants.remove(user)
    
    def getParticipants(self):
        return self.participants
    
    def getParticipantsStr(self):
        participant_names = ""
        for participant in self.participants:
            participant_names += participant.display_name + ", "
        return participant_names[:-2] #Remove the last comma (and space)

    def getEmbed(self):
        embedMeeting = discord.Embed(title=self.name, color=0x00ff00) 
        #Don't repeat the title
        desc = self.__repr__()
        for i in range(len(desc)):
            if (desc[i] == '\n'):
                desc = desc[i+1:]
                break
        embedMeeting.description = desc
        return embedMeeting

    def __eq__(self, other):
        return self.name == other.name

    def __le__(self, other):
        if(self.date == other.date):
            return self.time < other.time
        return self.date < other.date

    def __ge__(self, other):
        if(self.date == other.date):
            return self.time > other.time
        return self.date > other.date

    def __repr__(self):
        string = "{name}\n{hour:0>2}:{minute:0>2} {day:0>2}/{month:0>2}/{year:0>2}\nParticipants: {participants}\nDescription: {desc}\nAuto-Remind: {autoremind}"
        return string.format(name = self.name, hour = self.time.hour, minute = self.time.minute, day = self.date.day, month = self.date.month, year = self.date.year, participants = self.getParticipantsStr(), desc = self.desc, autoremind = "Yes" if self.auto_remind else "No")