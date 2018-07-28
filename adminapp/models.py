from djongo import models
from django.utils import timezone
from django import forms
from passlib.apps import custom_app_context as pwd_context
import os
import datetime

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/account/identicon.png')


# Create your models here.


class Student(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    fullname = models.CharField(max_length=300)
    hometown = models.TextField()
    birthday = models.DateField(default=timezone.now, editable=True)
    school = models.TextField()
    graduationtime = models.DateField(default=timezone.now, editable=True)
    face = models.ImageField(default=MEDIA_ROOT, upload_to='student/%Y/%m/%d/')
    email = models.EmailField(max_length=450)
    phone = models.CharField(max_length=100)
    coursecode = models.CharField(max_length=100, blank=True)
    studentcode = models.CharField(max_length=200, blank=True)
    accountcode = models.CharField(max_length=200, blank=True)
    createdate = models.DateTimeField(default=timezone.now, editable=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return u'%s' % self.fullname

    def delete(self, *args, **kwargs):
        for field_name in ['pk']:
            val = getattr(self, field_name, False)
            if val:
                student = Student.objects.filter(pk=val).first()
                storage, path = student.face.storage, student.face.path
                storage.delete(path)
        super(Student, self).delete(*args, **kwargs)

    def deleteimage(self, *args, **kwargs):
        for field_name in ['pk']:
            val = getattr(self, field_name, False)
            if val:
                student = Student.objects.filter(pk=val).first()
                storage, path = student.face.storage, student.face.path
                storage.delete(path)

    def saveupdate(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)

    def getall(self):
        return {
            "id": str(self.pk),
            "fullname": self.fullname,
            "hometown": self.hometown,
            "birthday": str(self.birthday),
            "school": self.school,
            "graduationtime": str(self.graduationtime),
            "face": str(self.face),
            "email": self.email,
            "phone": self.phone,
            "coursecode": self.coursecode,
            "studentcode": self.studentcode,
            "accountcode": self.accountcode,
            "createdate": str(self.createdate),
            "status": self.status
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'fullname', 'hometown',
            'birthday', 'school',
            'graduationtime', 'face',
            'email', 'phone',
            'createdate', 'status'
        )


class Teacher(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)
    account = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def getall(self):
        return {
            "id": str(self.pk),
            "fullname": self.fullname,
            "email": self.email,
            "account": self.account
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = (
            'fullname', 'email', 'account'
        )


class Course(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    namecourse = models.CharField(max_length=400)
    startdate = models.DateField(default=timezone.now, editable=True)
    enddate = models.DateField(default=timezone.now, editable=True)
    imagecourse = models.ImageField(default=MEDIA_ROOT, upload_to='course/%Y/%m/%d/')
    teacher = models.EmbeddedModelField(
        model_container=Teacher,
        model_form_class=TeacherForm
    )

    student = models.ArrayReferenceField(
        to=Student,
        on_delete=models.CASCADE,
    )
    coursecode = models.CharField(max_length=100)
    categorycourse = models.CharField(max_length=300, blank=True)
    createdate = models.DateField(default=timezone.now, editable=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return u'%s' % self.namecourse

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.imagecourse.storage, self.imagecourse.path
        super(Course, self).delete(*args, **kwargs)
        storage.delete(path)

    def getall(self):
        if self.student:
            return {
                "id": str(self._id),
                "namecourse": self.namecourse,
                "startdate": str(self.startdate),
                "enddate": str(self.enddate),
                "imagecourse": str(self.imagecourse),
                "teacher": self.teacher.getall(),
                "student": []
            }
        else:
            return {
                "id": str(self._id),
                "namecourse": self.namecourse,
                "startdate": str(self.startdate),
                "enddate": str(self.enddate),
                "imagecourse": str(self.imagecourse),
                "teacher": self.teacher.getall(),
                "student": [val.getall() for val in self.student]
            }

    def getallc(self):
        return {
            "id": str(self._id),
            "namecourse": self.namecourse,
            "startdate": str(self.startdate),
            "enddate": str(self.enddate),
            "imagecourse": str(self.imagecourse),
            "teacher": self.teacher.getall()
        }


# Comment teacher and student

class EvaluateCommentUsers(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    userscomment = models.CharField(max_length=300)  # id student
    rolecomment = models.CharField(max_length=300)  # id teacher comment
    coursecomment = models.CharField(max_length=500)  # id course
    contentcomment = models.TextField(max_length=800)  # content

    def __str__(self):
        return self.userscomment

    def getall(self):
        return {
            "id": str(self.pk),
            "userscomment": self.userscomment,
            "rolecomment": self.rolecomment,
            "coursecomment": self.coursecomment,
            "contentcomment": self.contentcomment
        }


# End comment teacher and student

# Upload file teacher

class UploadFileUsers(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=600)
    usersupload = models.CharField(max_length=300)
    coursecode = models.CharField(max_length=500)
    contentfile = models.FileField(default=MEDIA_ROOT, upload_to='files/%Y/%m/%d/')
    comment = models.TextField(max_length=900)
    created = models.DateField(default=timezone.now, editable=True)

    def __str__(self):
        return self.usersupload

    def getall(self):
        return {
            "id": str(self.pk),
            "name": self.name,
            "usersupload": self.usersupload,
            "coursecode": self.coursecode,
            "contentfile": str(self.contentfile),
            "comment": self.comment,
            "created": str(self.created)
        }

    def delete(self, *args, **kwargs):
        storage, path = self.contentfile.storage, self.contentfile.path
        super(UploadFileUsers, self).delete(*args, **kwargs)
        storage.delete(path)


# Upload file teacher

# Category course

class SubCateCourse(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    namesubcourse = models.CharField(max_length=400)
    subcoursecode = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.namesubcourse

    class Meta:
        abstract = True


class SubCateCourseForm(forms.ModelForm):
    class Meta:
        model = SubCateCourse
        fields = (
            'namesubcourse', 'subcoursecode'
        )


class CategoryCourse(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    namecourse = models.CharField(max_length=400)
    subcourse = models.ArrayModelField(model_container=SubCateCourse,
                                       model_form_class=SubCateCourseForm, blank=True)
    createdate = models.DateField(default=timezone.now, editable=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.namecourse

    def getall(self):
        return {
            "id": str(self.pk),
            "namecourse": self.namecourse,
            "subcourse": [{"namesubcourse": val.namesubcourse, "subcoursecode": str(val.subcoursecode)} for val
                          in
                          self.subcourse],
            "createdate": str(self.createdate),
            "status": self.status
        }
