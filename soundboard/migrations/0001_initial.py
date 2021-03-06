# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-13 02:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('text', models.CharField(max_length=280, null=True)),
                ('sound_file', models.FileField(upload_to='sounds/')),
                ('image_file', models.FileField(blank=True, null=True, upload_to='sound_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Soundboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='SoundboardAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soundboard.Sound')),
                ('soundboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soundboard.Soundboard')),
            ],
        ),
        migrations.AddField(
            model_name='soundboard',
            name='sounds',
            field=models.ManyToManyField(through='soundboard.SoundboardAssociation', to='soundboard.Sound'),
        ),
        migrations.AddField(
            model_name='soundboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
