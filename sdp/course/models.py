from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# auxiliary class
# for encapsulate all direct operaions in database


class StaffControl():

    class Meta:
        abstract = True

    @staticmethod
    def getUser(id):
        return User.objects.get(pk=id)

    @staticmethod
    def getUserByName(name):
        try:
            x = User.objects.get(username=name)
            return x
        except User.DoesNotExist:
            return None


class HRControl(StaffControl):

    @staticmethod
    def viewAllParticipants():
        menu = dict()
        for p in Participant.objects.all():
            menu[p.user.id] = p
        return menu

    @staticmethod
    def viewParticipant(participant_id):
        participant = Participant.objects.get(user__pk=participant_id)
        return participant


class AdministratorControl(StaffControl):

    @staticmethod
    def viewAllStaffs():
        return User.objects.all()

    @staticmethod
    def designate(user):
        g = Group.objects.get(name='Instructor')
        g.user_set.add(user)
        instructor = Instructor.objects.create(user=user)


class CategoryControl():

    @staticmethod
    def addCategory(category_name):
        category = Category.objects.create(name=category_name)

    @staticmethod
    def viewCategories(type, instance):
        if type == 'Administrator':
            menu = super(Administrator, instance).viewCategories()
        elif type == 'HR':
            menu = super(HR, instance).viewCategories()
        for c in Category.objects.all():
            menu[c] = Course.objects.filter(category=c).count()
        return menu

    @staticmethod
    def deleteCategory(category_id):
        category = Category.objects.get(id=category_id)
        num = Course.objects.filter(category=category).count()
        if num == 0:
            category.delete()
            return True
        else:
            return False


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
        if CurrentEnrollment.objects.filter(participant=self, course__id=course_id).exists():
            currrentEnrollment = CurrentEnrollment.objects.get(
                participant=self, course__id=course_id)
            menu = super(Participant, self).viewCourse(course_id)
            menu['is_enrolled'] = True
            menu['has_finished'] = False
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
        elif HistoryEnrollment.objects.filter(participant=self, course__id=course_id).exists():
            historyEnrollment = HistoryEnrollment.objects.get(
                participant=self, course__id=course_id)
            menu = super(Participant, self).viewCourse(course_id)
            menu['is_enrolled'] = False
            menu['has_finished'] = True
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
        else:
            menu = super(Participant, self).viewCourse(course_id)
            menu['is_enrolled'] = False
            menu['has_finished'] = False
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
            CurrentEnrollment.objects.create(course=course, participant=self)
            return True

    def drop(self):
        if CurrentEnrollment.objects.filter(participant__id=self.pk).exists():
            CurrentEnrollment.objects.get(participant__id=self.pk).delete()
            return True
        else:
            return False

    def finishCourse(self):
        current = CurrentEnrollment.objects.get(participant__id=self.pk)
        HistoryEnrollment.objects.create(
            course=current.course, participant=self, date_of_completion=date.today())
        current.delete()


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
        # checking if opening course is valid, which means that a course must have at least
        # one module and every module must have at least one component
        if Module.objects.filter(course__pk=course_id).count() == 0:
            return False
        for module in Module.objects.filter(course__pk=course_id):
            if Component.objects.filter(module__pk=module.id).count() == 0:
                return False
        course = Course.objects.get(pk=course_id)
        if course.instructor.id == self.pk:
            course.is_open = True
            course.save()
            return True
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
        if component_content_type == '2':
            text = Text.objects.create(content=component_content)
            component = Component.objects.create(name=component_name, localPosition=localPosition,
                                                 module=parent_module, content_type=component_content_type, content_object=text)
        elif component_content_type == '4':
            youtube = YouTube.objects.create(content=component_content)
            component = Component.objects.create(name=component_name, localPosition=localPosition,
                                                 module=parent_module, content_type=component_content_type, content_object=youtube)
        elif component_content_type == '1':
            _file = File.objects.create(
                content=component_content, content_file=content_file)
            component = Component.objects.create(name=component_name, localPosition=localPosition,
                                                 module=parent_module, content_type=component_content_type, content_object=_file)
            return component

        elif component_content_type == '3':
            image = Image.objects.create(
                content=component_content, content_file=content_file)
            component = Component.objects.create(name=component_name, localPosition=localPosition,
                                                 module=parent_module, content_type=component_content_type, content_object=image)
            return component

    def deleteComponent(self, component_id):
        # firstly change all components below itself, make their
        # localPosition-1
        component = Component.objects.get(pk=component_id)
        for component_ in Component.objects.filter(module__id=component.module.id, localPosition__gt=component.localPosition):
            component_.localPosition -= 1
            component_.save()
        component.delete()

    def deleteModule(self, module_id):
        module = Module.objects.get(pk=module_id)
        for module_ in Module.objects.filter(course__id=module.course.id, localPosition__gt=module.localPosition):
            module_.localPosition -= 1
            module_.save()
        module.delete()


class Administrator(Staff):

    def viewCategories(self):
        return CategoryControl.viewCategories('Administrator', self)

    def createCategory(self, category_name):
        CategoryControl.addCategory(category_name)

    def deleteCategory(self, category_id):
        return CategoryControl.deleteCategory(category_id)

    def viewAllUsers(self):
        return AdministratorControl.viewAllStaffs()

    def getUser(self, id):
        return StaffControl.getUser(id)

    def getUserByName(self, name):
        return StaffControl.getUserByName(name)

    def designateInstructor(self, user):
        AdministratorControl.designate(user)


class HR(Staff):

    def viewCategories(self):
        return CategoryControl.viewCategories('HR', self)

    def viewAllParticipants(self):

        return HRControl.viewAllParticipants()

    def viewParticipant(self, participant_id):
        return HRControl.viewParticipant(participant_id)


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

    def updateLocalPostion(self, newLocalPostion):
        self.localPosition = newLocalPostion
        self.save()


class Component(models.Model):
    name = models.CharField(max_length=200)
    localPosition = models.IntegerField(default=0)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, default=None)  # many-to-one
    CONTENT_TYPES = (
        (u'1', u'File'),
        (u'2', u'Text'),
        (u'3', u'Image'),
        (u'4', u'YouTube'),
    )
    content_type = models.CharField(
        max_length=1, choices=CONTENT_TYPES, default=None)
    # Below the mandatory fields for generic relation
    _content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('_content_type', 'object_id')

    def __str__(self):
        return self.name

    def updateLocalPostion(self, newLocalPostion):
        self.localPosition = newLocalPostion
        self.save()


class Text(models.Model):
    # component = GenericRelation(Component)
    content = models.TextField()


class File(models.Model):
    # component = GenericRelation(Component)
    content = models.TextField()
    content_file = models.FileField(
        upload_to='uploads/files/%Y/%m/%d/', null=True)


class Image(models.Model):
    # component = GenericRelation(Component)
    content = models.TextField()
    content_file = models.FileField(
        upload_to='uploads/images/%Y/%m/%d/', null=True)


class YouTube(models.Model):
    # component = GenericRelation(Component)
    content = models.TextField()


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
    current_module_num = models.IntegerField(default=1)
    current_component_num = models.IntegerField(default=1)

    def getInfo(self):
        return str(self.current_model_num) + '.' + str(self.current_component_num)
