from djongo import models
from django.utils import timezone
from django import forms
from passlib.apps import custom_app_context as pwd_context
import os
from datetime import datetime

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/account/identicon.png')


# Create your models here.

class Role(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    createdate = models.DateTimeField(default=timezone.now, editable=True)

    def __str__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        for field_name in ['name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, str(val).upper())
        super(Role, self).save(*args, **kwargs)


class InfoTeacher(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)

    class Meta:
        abstract = True


class InfoTeacherForm(forms.ModelForm):
    class Meta:
        model = InfoTeacher
        fields = (
            'fullname', 'email'
        )


class Account(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    image = models.ImageField(default=MEDIA_ROOT, upload_to='account/%Y/%m/%d/')
    password = models.CharField(max_length=450)
    info = models.EmbeddedModelField(model_container=InfoTeacher, model_form_class=InfoTeacherForm, blank=True)
    createdate = models.DateTimeField(default=timezone.now, editable=True)
    status = models.BooleanField(default=True)

    objects = models.DjongoManager()

    def __str__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        for field_name in ['password']:
            val = getattr(self, field_name, False)
            if val:
                enc_password = pwd_context.hash(val)
                setattr(self, field_name, enc_password)
        super(Account, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for field_name in ['pk']:
            val = getattr(self, field_name, False)
            if val:
                account = Account.objects.filter(pk=val).first()
                storage, path = account.image.storage, account.image.path
                storage.delete(path)
        super(Account, self).delete(*args, **kwargs)

    def deleteimage(self, *args, **kwargs):
        for field_name in ['pk']:
            val = getattr(self, field_name, False)
            if val:
                account = Account.objects.filter(pk=val).first()
                storage, path = account.image.storage, account.image.path
                storage.delete(path)

    def saveupdate(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

    def getall(self):
        return {
            "id": str(self._id),
            "name": self.name,
            "rolename": self.role.name,
            "roleid": str(self.role._id),
            "image": self.image.url,
            "infofullname": self.info.fullname,
            "infoname": self.info.email,
            "createdate": str(self.createdate),
            "status": self.status
        }

    def verify_password(self, raw_password):
        return pwd_context.verify(raw_password, self.password)
