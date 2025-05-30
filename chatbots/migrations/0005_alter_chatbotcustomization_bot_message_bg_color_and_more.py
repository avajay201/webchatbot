# Generated by Django 5.2.1 on 2025-05-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbots', '0004_chatbot_last_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='bot_message_bg_color',
            field=models.CharField(default='#334155', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='chat_close_btn_color',
            field=models.CharField(default='#f87171', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='chat_icon_bg_color',
            field=models.CharField(default='#1e3a8a', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='header_bg_color',
            field=models.CharField(default='#0f172a', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='header_text_color',
            field=models.CharField(default='#f1f5f9', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='input_border_color',
            field=models.CharField(default='#475569', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='input_color',
            field=models.CharField(default='#f8fafc', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='input_container_bg_color',
            field=models.CharField(default='#0f172a', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='input_placeholder_color',
            field=models.CharField(default='#94a3b8', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='msg_box_bg_color',
            field=models.CharField(default='#1e293b', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='scrollbar_color',
            field=models.CharField(default='#64748b', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='send_btn_color',
            field=models.CharField(default='#38bdf8', max_length=7),
        ),
        migrations.AlterField(
            model_name='chatbotcustomization',
            name='user_message_bg_color',
            field=models.CharField(default='#2563eb', max_length=7),
        ),
    ]
