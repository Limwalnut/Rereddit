# Generated by Django 2.1 on 2018-09-24 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parentCommentID', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('filePath', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('username', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.File')),
                ('threadId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Thread')),
            ],
        ),
        migrations.CreateModel(
            name='ThreadTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Tag')),
                ('threadId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Thread')),
            ],
        ),
        migrations.AddField(
            model_name='commenttag',
            name='tagId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Tag'),
        ),
        migrations.AddField(
            model_name='commentfile',
            name='fileId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.File'),
        ),
        migrations.AddField(
            model_name='comment',
            name='threadID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Thread'),
        ),
    ]
