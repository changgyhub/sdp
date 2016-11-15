from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many-to-one
    last_login_type = models.CharField(max_length=20, default="Staff")

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def viewCategories(self):
        menu = dict()
        return menu

    def viewCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        menu = dict()
        menu['name'] = course.name
        menu['category'] = course.category
        menu['instructor'] = course.instructor
        menu['description'] = course.description
        menu['is_open'] = course.is_open
        return menu


class Participant(Staff):

    def viewCategories(self):
        menu = super(Participant, self).viewCategories()
        for c in Category.objects.all():
            menu[c] = Course.objects.filter(category=c, is_open=True).count()
        return menu

    def viewCourse(self, course_id):
        # TODO: implement more in next iteration
        try:
            currrentEnrollment = CurrentEnrollment.objects.get(
                participant=self, course__id=course_id)
            menu = super(Participant, self).viewCourse(course_id)
            menu['is_enrolled'] = True
            menu['module'] = dict()
            module_list = list()
            for module in Module.objects.filter(course__id=course_id):
                menu['module'][module] = list()
                module_list.append(module)
            for component in Component.objects.all():
                for module in module_list:
                    if component.module.id == module.id:
                        menu['module'][module].append(component)
            return menu
        except ObjectDoesNotExist:
            menu = super(Participant, self).viewCourse(course_id)
            menu['is_enrolled'] = False
            return menu

    def getHistoryInfo(self):
        menu = dict()
        for history in HistoryEnrollment.objects.filter(participant__id=self.pk):
            menu[history.getCourse()] = history.getInfo()
        return menu

    def getCurrentInfo(self):
        if CurrentEnrollment.objects.filter(participant__id=self.pk).exists():
            currentEnrollment = CurrentEnrollment.objects.get(
                participant__id=self.pk)
            return currentEnrollment.course
        return None

    def enroll(self, course_id):
        if CurrentEnrollment.objects.filter(participant__id=self.pk).exists():
            return False
        else:
            course = Course.objects.get(pk=course_id)
            CurrentEnrollment.objects.create(
                course=course, participant=self, progress="0")
            return True


class Instructor(Staff):

    def viewCategories(self):
        menu = super(Instructor, self).viewCategories()
        for c in Category.objects.all():
            menu[c] = Course.objects.filter(Q(category=c) & (
                Q(is_open=True) | Q(instructor=self))).count()
        return menu

    def viewCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id != self.pk:
            # call supermethod if it is not his course
            return super(Instructor, self).viewCourse(course_id)
        else:
            menu = super(Instructor, self).viewCourse(course_id)
            menu['module'] = dict()
            module_list = list()
            for module in Module.objects.filter(course__id=course_id):
                menu['module'][module] = list()
                module_list.append(module)
            for component in Component.objects.all():
                for module in module_list:
                    if component.module.id == module.id:
                        menu['module'][module].append(component)
            return menu

    def viewMyCourses(self):
        menu = dict()
        for category in Category.objects.all():
            menu[category.name] = list()
        for course in Course.objects.filter(instructor__id=self.pk):
            menu[course.category.name].append(course)
        return menu

    def openCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id == self.pk:
            course.is_open = True
            course.save()
        else:
            print("TODO")
            # TODO: fail to open a course
            #       this should not happen actually

    def closeCourse(self, course_id):
        course = Course.objects.get(pk=course_id)
        if course.instructor.id == self.pk:
            course.is_open = False
            course.save()
        else:
            print("TODO")

    def createCourse(self, course_name, course_info, course_category):
        course = Course.objects.create(category=course_category,
                                       name=course_name, description=course_info, instructor=self)
        # is_open = False as default

    def createModule(self, course_id, module_name, localPosition):
        parent_course = Course.objects.get(pk=course_id)
        module = Module.objects.create(
            course=parent_course, name=module_name, localPosition=localPosition)

    def createComponent(self, module_id, component_name, component_content_type, component_content, content_file=None, localPosition=0):
        parent_module = Module.objects.get(pk=module_id)
        if component_content_type == 2:
            component = Component.objects.create(name=component_name, content=component_content,
                                                 content_type=component_content_type, module=parent_module, localPosition=localPosition)
        else:
            component = Component.objects.create(name=component_name, content=component_content,
                                                 content_file=component_content, content_type=component_content_type, module=parent_module, localPosition=localPosition)
            return component

    def deleteComponent(self, component_id):
        # assume that the course is already the instructor's
        Component.objects.get(pk=component_id).delete()


class Administrator(Staff):

    def viewCategories(self):
        menu = super(Administrator, self).viewCategories()
        for c in Category.objects.all():
            menu[c] = Course.objects.filter(category=c, is_open=True).count()
        return menu
    def createCategory(self, category_name):
        category = Category.objects.create(name=category_name)

class HR(Staff):

    def viewCategories(self):
        menu = super(HR, self).viewCategories()
        for c in Category.objects.all():
            menu[c] = Course.objects.filter(category=c).count()
        return menu

    def viewAllParticipants(self):
        menu = dict()
        for p in Participant.objects.all():
            menu[p.user.id] = p
        return menu

    def viewParticipant(self, participant_id):
        participant = Participant.objects.get(user__pk=participant_id)
        return participant


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    is_open = models.BooleanField(default=False)  # default set to false
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE)  # many-to-one
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)  # many-to-one
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many-to-one
    localPosition = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.CharField(max_length=200)
    CONTENT_TYPES = (
        (u'1', u'File'),
        (u'2', u'Text'),
        (u'3', u'Image'),
    )  # need to be changed later on
    content_type = models.CharField(
        max_length=1, choices=CONTENT_TYPES, default=None)
    content = models.CharField(max_length=200, default=None, null=True)
    content_file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True)
    localPosition = models.IntegerField(default=0)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, default=None)  # many-to-one

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many-to-one
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE)  # many-to-one

    class Meta:
        abstract = True

    def __str__(self):
        return self.course.name + ' - ' + str(self.participant)

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
