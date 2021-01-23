"""
Object template for schedules. Currently
pretty basic and lacking in details (especially
in how participants will be stored).
"""
import datetime

class Meeting:
    def __init__(self, name):
        self.name = name
        self.participants = []
        self.time = datetime.time(0,0,0)
        self.date = datetime.date(2000, 1, 1)
        self.desc = ""
        self.autoRemind = False
    
    def setTime(self, time):
        self.time = time
    
    def setDate(self, date):
        self.date = date
    
    def setDesc(self, desc):
        self.desc = desc
    
    def setAutoRemind(self, autoRemind):
        self.autoRemind = autoRemind

    def addParticipant(self, user):
        self.participants.append(user)
    
    def removeParticipant(self, user):
        self.participants.remove(user)
    