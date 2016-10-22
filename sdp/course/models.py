from django.db import models

# set for debug
DEBUG = False


class Staff(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def viewCatagories(self):
        menu = dict()
        for catagory in Catagory.objects.all():
            menu[catagory.name] = list()
        for course in Course.objects.all():
            if course.is_open == True:
                menu[course.catagory.name].append(course)
        return menu

    def viewCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        menu = dict()
        menu['name'] = course.name
        menu['catagory'] = course.catagory.name
        menu['instructor'] = course.instructor.name
        menu['description'] = course.description
        return menu


class Participant(Staff):

    def viewCourse(self, course_id):
        # TODO: implement in next iteration
        return super(Participant, self).viewCourse(course_id)

    def getHistoryInfo(self):
        menu = dict()
        for history in HistoryEnrollment.objects.all():
            if history.participant.id == self.pk:
                menu[history.getCourse()] = history.getInfo()
        return menu

    def getCurrentInfo(self):
        menu = dict()
        for current in CurrentEnrollment.objects.all():
            if current.participant.id == self.pk:
                menu[current.getCourse()] = current.getInfo()
                return menu  # because participant can only have one current course


class Instructor(Staff):

    def viewCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id != self.pk:
            # call supermethod if it is not his course
            return super(Instructor, self).viewCourse(course_id)
        else:
            menu = dict()
            menu['name'] = course.name
            menu['catagory'] = course.catagory.name
            menu['instructor'] = course.instructor.name
            menu['description'] = course.description
            menu['module'] = dict()
            module_list = list()
            for module in Module.objects.all():
                if module.course.id == course_id:
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
        for course in Course.objects.all():
            if course.instructor.id == self.pk:
                menu[course.catagory.name].append(course)
        return menu

    def openCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id == self.pk:
            return "TODO: Wang Haicheng"

    def createCourse(self, course_name, course_info, course_catagory):
        course = Course.objects.create(catagory = course_catagory,
                name=course_name, description=course_info, instructor = self)
                # is_open = False as default
        # here we better do some validation before we got the right

        #
        course.save()
        if (DEBUG):
            Course.objects.value_list('name', flat=True)
        return "TODO: Wang Haicheng"

    def createModule(self, course_id, module_name):
        return "TODO: Yan Kai"

    def createComponent(self, module_id, component_name, component_content, component_content_type):
        return "TODO: Huang Qingwei"


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
    content = models.CharField(max_length=200)
    CONTENT_TYPES = (
        (u'1', u'File'),
        (u'2', u'Text'),
        (u'3', u'Image'),
    )  # need to be changed later on
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES)
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
