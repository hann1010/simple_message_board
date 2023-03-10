# Generated by Django 3.2 on 2023-01-01 18:44

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(blank=True, max_length=100)),
                ('origin_post_id', models.IntegerField(default=0)),
                ('content', ckeditor.fields.RichTextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_last_save', models.DateTimeField(auto_now=True)),
                ('author_name', models.CharField(blank=True, max_length=100)),
                ('author_nickname', models.CharField(blank=True, max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
