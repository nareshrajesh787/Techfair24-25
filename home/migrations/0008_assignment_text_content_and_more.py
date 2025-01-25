# Generated by Django 5.1.2 on 2025-01-25 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_assignment_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='text_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_assignment',
            field=models.FileField(blank=True, null=True, upload_to='assignments/'),
        ),
    ]
