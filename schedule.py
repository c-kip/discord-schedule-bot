"""
Object template for schedules. Currently
pretty basic and lacking in details (especially
in how participants will be stored).
"""
import datetime

class Meeting:
    def __init__(self, name, time = datetime.time(0,0,0), date = datetime.date(2000, 1, 1), participants = [], message = "", desc = "", auto_remind = False):
        self.name = name
        self.time = time
        self.date = date
        self.participants = participants
        self.message = message
        self.desc = desc
        self.auto_remind = auto_remind
    
    def getName(self):
        return self.name

    def setTime(self, time):
        self.time = time
    
    def getTime(self):
        return self.time.strftime('%H:%M')
    
    def setDate(self, date):
        self.date = date
    
    def getDate(self):
        return self.date.strftime('%B %d, %Y')

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
        self.participants.append(user)
    
    def removeParticipant(self, user):
        self.participants.remove(user)
    
    def getParticipants(self):
        return self.participants

    def __repr__(self):
        participant_names = []
        for name in self.participants:
            participant_names.append(name.name)
        return "The meeting {} will happen at {} on {}:\nDescription: {}\nParticipants: {}".format(self.name, self.time, self.date, self.desc, ", ".join(participant_names))