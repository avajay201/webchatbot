# Generated by Django 5.2.1 on 2025-05-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbots', '0003_chatbot_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='last_used',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
