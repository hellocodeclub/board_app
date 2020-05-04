# Generated by Django 3.0.5 on 2020-05-03 11:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_title', models.CharField(max_length=300)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('estimated_hours', models.IntegerField(blank=True)),
                ('status', models.CharField(max_length=30)),
                ('assigned_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Account')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='CycleTaskAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.Cycle')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.Task')),
            ],
        ),
    ]
