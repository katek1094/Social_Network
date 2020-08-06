# Generated by Django 3.0.7 on 2020-07-24 20:59

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(default='default_profile_pic.jpg', upload_to=app.models.user_directory_path)),
                ('city', models.CharField(blank=True, max_length=40)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('nickname', models.CharField(blank=True, max_length=24)),
                ('friends', models.ManyToManyField(related_name='_userprofile_friends_+', through='app.Friendship', to='app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=app.models.image_directory_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Post')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='app.UserProfile'),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_receiver', to='app.UserProfile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendrequest_sender', to='app.UserProfile')),
            ],
        ),
    ]
