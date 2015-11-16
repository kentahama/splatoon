from django.db import models

ROOM_CHOICES = (
    ('T', 'Tag'),
    ('P', 'Private'),
)
MEMBER_MAX_OF = {
    'T': 4,
    'P': 8,
}

class Room(models.Model):
    type = models.CharField(max_length=1, choices=ROOM_CHOICES) 
    createdate = models.DateField("date created")
    comment = models.TextField()
    def creator(self):
        return self.user_set.get(is_creator=True)
    def members(self):
        return self.user_set.all()
    def member_num(self):
        return self.user_set.count()        
    def member_max(self):
        return MEMBER_MAX_OF[self.type]    
    def remaining(self):
        return self.member_max() - self.member_num()
    def is_full(self):
        return self.member_num() >= self.member_max()
    def __unicode__(self):
        return str(self.id) + ", " + self.type

class User(models.Model):
    room = models.ForeignKey(Room)
    name = models.CharField(max_length=32)
    is_creator = models.BooleanField()
    def __unicode__(self):
        return self.name
