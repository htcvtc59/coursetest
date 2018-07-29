# Generated by Django 2.0.6 on 2018-07-29 10:30

import adminapp.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryCourse',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('namecourse', models.CharField(max_length=400)),
                ('subcourse', djongo.models.fields.ArrayModelField(blank=True, model_container=adminapp.models.SubCateCourse, model_form_class=adminapp.models.SubCateCourseForm)),
                ('createdate', models.DateField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('namecourse', models.CharField(max_length=400)),
                ('startdate', models.DateField(default=django.utils.timezone.now)),
                ('enddate', models.DateField(default=django.utils.timezone.now)),
                ('imagecourse', models.ImageField(default='/Users/oh/Desktop/djangoCourse/media/account/identicon.png', upload_to='course/%Y/%m/%d/')),
                ('teacher', djongo.models.fields.EmbeddedModelField(model_container=adminapp.models.Teacher, model_form_class=adminapp.models.TeacherForm, null=True)),
                ('coursecode', models.CharField(max_length=100)),
                ('categorycourse', models.CharField(blank=True, max_length=300)),
                ('createdate', models.DateField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluateCommentUsers',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('userscomment', models.CharField(max_length=300)),
                ('rolecomment', models.CharField(max_length=300)),
                ('coursecomment', models.CharField(max_length=500)),
                ('contentcomment', models.TextField(max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=300)),
                ('hometown', models.TextField()),
                ('birthday', models.DateField(default=django.utils.timezone.now)),
                ('school', models.TextField()),
                ('graduationtime', models.DateField(default=django.utils.timezone.now)),
                ('face', models.ImageField(default='', upload_to='student/%Y/%m/%d/')),
                ('email', models.EmailField(max_length=450)),
                ('phone', models.CharField(max_length=100)),
                ('coursecode', models.CharField(blank=True, max_length=100)),
                ('studentcode', models.CharField(blank=True, max_length=200)),
                ('accountcode', models.CharField(blank=True, max_length=200)),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFileUsers',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=600)),
                ('usersupload', models.CharField(max_length=300)),
                ('coursecode', models.CharField(max_length=500)),
                ('contentfile', models.FileField(default='/Users/oh/Desktop/djangoCourse/media/account/identicon.png', upload_to='files/%Y/%m/%d/')),
                ('comment', models.TextField(max_length=900)),
                ('created', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, to='adminapp.Student'),
        ),
    ]
