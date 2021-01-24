"""
Object template for schedules. Currently
pretty basic and lacking in details (especially
in how participants will be stored).
"""
import datetime
import discord

class Meeting:
    def __init__(self, name, time = datetime.time(0,0,0), duration = datetime.timedelta(hours=1), date = datetime.date(2000, 1, 1), participants = [], desc = "", auto_remind = False):
        self.name = name
        self.time = time
        self.duration = duration
        self.date = date
        self.datetime = datetime.datetime.combine(date, time)
        self.participants = participants
        self.desc = desc
        self.auto_remind = auto_remind
        self.message = ""
        self.admins = []
    
    def getName(self):
        return self.name

    def setTime(self, time):
        self.time = time
        self.datetime = datetime.datetime.combine(self.date, self.time)
    
    def getTime(self):
        return self.time
    
    def setDuration(self, duration):
        if (duration > datetime.timedelta(0,0,0)):
            self.duration = duration

    def getDuration(self):
        return self.duration
    
    def getEndDateTime(self):
        return self.datetime + self.duration

    def setDate(self, date):
        self.date = date
        self.datetime = datetime.datetime.combine(self.date, self.time)
    
    def getDate(self):
        return self.date

    def getDateTime(self):
        return self.datetime

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

    def addAdmin(self, user):
        if (not(user in self.admins)):
            self.admins.append(user)
            self.addParticipant(user)
            return True
        return False
    
    def removeAdmin(self, user):
        if (user in self.admins and len(self.admins) > 1):
            self.admins.remove(user)
            return True
        return False

    def getAdmin(self):
        return self.admins

    def getAdminsStr(self):
        admin_names = ""
        for admin in self.admins:
            admin_names += admin.display_name + ", "
        return admin_names[:-2]

    def addParticipant(self, user):
        #Only add if they haven't been already
        if (not(user in self.participants)):
            self.participants.append(user)
            return True
        return False
    
    def removeParticipant(self, user):
        self.participants.remove(user)
        return True
    
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
        string = "{name}\nStart: {hour:0>2}:{minute:0>2} {day:0>2}/{month:0>2}/{year:0>2}\nEnd: {end_hour:0>2}:{end_minute:0>2} {end_day:0>2}/{end_month:0>2}/{end_year:0>2}\nAdmins: {admins}\nParticipants: {participants}\nDescription: {desc}\nAuto-Remind: {autoremind}"
        return string.format(name = self.name, hour = self.time.hour, minute = self.time.minute, day = self.date.day, month = self.date.month, year = self.date.year,
                             end_hour = self.getEndDateTime().hour, end_minute = self.getEndDateTime().minute, end_day = self.getEndDateTime().day, end_month = self.getEndDateTime().month,
                             end_year = self.getEndDateTime().year, admins = self.getAdminsStr(), participants = self.getParticipantsStr(), desc = self.desc, autoremind = "Yes" if self.auto_remind else "No")