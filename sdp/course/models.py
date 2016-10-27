from django.db import models
from django.contrib.auth.models import User

class Staff(User):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def viewCatagories(self):
        menu = dict()
        for catagory in Catagory.objects.all():
            menu[catagory.name] = list()
        for course in Course.objects.filter(is_open = True):
            menu[course.catagory.name].append(course)
        return menu

    def viewCourse(self, course_id):
        course = Course.objects.get(pk = course_id)
        menu = dict()
        menu['name'] = course.name
        menu['catagory'] = course.catagory
        menu['instructor'] = course.instructor
        menu['description'] = course.description
        menu['is_open'] = course.is_open
        return menu

class Participant(Staff):

    def viewCourse(self, course_id):
        # TODO: implement in next iteration
        return super(Participant, self).viewCourse(course_id)

    def getHistoryInfo(self):
        menu = dict()
        for history in HistoryEnrollment.objects.filter(participant__id = self.pk):
            menu[history.getCourse()] = history.getInfo()
        return menu

    def getCurrentInfo(self):
        menu = dict()
        for current in CurrentEnrollment.objects.get(participant__id = self.pk):
            # we use get here because there can only be one current course
            menu[current.getCourse()] = current.getInfo()
        return menu


class Instructor(Staff):

    def viewCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id != self.pk:
            # call supermethod if it is not his course
            return super(Instructor, self).viewCourse(course_id)
        else:
            menu = super(Instructor, self).viewCourse(course_id)
            menu['module'] = dict()
            module_list = list()
            for module in Module.objects.filter(course__id = course_id):
                menu['module'][module] = list()
                module_list.append(module)
            for component in Component.objects.all():
                for module in module_list:
                    if component.module.id == module.id:
                        menu['module'][module].append(component)
            return menu

    def viewMyCourses(self):
        menu = dict()
        for catagory in Catagory.objects.all():
            menu[catagory.name] = list()
        for course in Course.objects.filter(instructor__id = self.pk):
            menu[course.catagory.name].append(course)
        return menu


    def openCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id == self.pk:
            course.is_open = True;
            course.save()
        else:
            print ("TODO")
            # TODO: fail to open a course
            #       this should not happen actually

    def createCourse(self, course_name, course_info, course_catagory):
        course = Course.objects.create(catagory = course_catagory,
                name=course_name, description=course_info, instructor = self)
                # is_open = False as default

    def createModule(self, course_id, module_name):
        parent_course = Course.objects.get(pk = course_id)
        module = Module.objects.create(course = parent_course, name = module_name)

    def createComponent(self, module_id, component_name, component_content_type, component_content):
        parent_module = Module.objects.get(pk = module_id)
        component = Component.objects.create(name = component_name, content = component_content,
                content_type = component_content_type, module = parent_module)

class Catagory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    is_open = models.BooleanField(default=False)  # default set to false
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE)  # many-to-one
    catagory = models.ForeignKey(
        Catagory, on_delete=models.CASCADE)  # many-to-one
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many-to-one

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.CharField(max_length=200)
    CONTENT_TYPES = (
        (u'1', u'File'),
        (u'2', u'Text'),
        (u'3', u'Image'),
    )  # need to be changed later on
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES)
    content = models.CharField(max_length=200)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)  # many-to-one

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many-to-one
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE)  # many-to-one

    class Meta:
        abstract = True

    def getCourse(self):
        return self.course

    def getInfo(self):
        return None


class HistoryEnrollment(Enrollment):
    date_of_completion = models.DateField()

    def getInfo(self):
        return self.date_of_completion


class CurrentEnrollment(Enrollment):
    progress = models.CharField(max_length=200)  # need to be changed later on

    def getInfo(self):
        return self.progress
