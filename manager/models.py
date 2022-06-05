from django.db import models

# Create your models here.
branches = (
    ('CSE','Computer Science Engineering'),
    ('ECE','Electronic Computer Engineering'),
    ('EEE','Electronic and Electrical Engineering'),
    ('Mech','Mechanical Engineering'),
    ('Civil','Civil Engineering'),
    ('IT','Information Technology')
    )

class StudentsList(models.Model):
    studentid = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=5,choices=branches,default=None)
    email_address = models.EmailField()
    mail_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.studentid + "  |  " +self.name + "  |  " + self.email_address + "  |  " +self.branch