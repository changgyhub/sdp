from django.db import models
class Staff(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    class Meta:
        abstract = True
    def __str__(self):
        return self.name
class Participant(Staff):
    name = models.CharField(max_length=200)
class Instructor(Staff):
    name = models.CharField(max_length=200)
class Catagory(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=200)
    is_open = models.BooleanField(default=False) # default set to false
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE) # many-to-one
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE) # many-to-one
    description = models.CharField(max_length=2000)
    def __str__(self):
        return self.name
class Module(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # many-to-one
    def __str__(self):
        return self.name
class Component(models.Model):
    name = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    CONTENT_TYPES = (
        (u'1', u'File'),
        (u'2', u'Text'),
        (u'3', u'Image'),
    ) # need to be changed later on
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES)
    module = models.ForeignKey(Module, on_delete=models.CASCADE) # many-to-one
    def __str__(self):
        return self.name
class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # many-to-one
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE) # many-to-one
    class Meta:
        abstract = True
class HistoryEnrollment(Enrollment):
    date_of_completion = models.DateField()
class CurrentEnrollment(Enrollment):
    progress = models.CharField(max_length=200) # need to be changed later on
