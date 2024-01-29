# Generated by Django 3.1.2 on 2023-10-26 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20231026_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioRecording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('audio_file', models.FileField(upload_to='audio_recordings/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
