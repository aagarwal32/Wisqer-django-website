# Generated by Django 4.2.15 on 2024-10-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0004_question_question_body_reply_reply_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reply",
            name="reply_body",
        ),
        migrations.AlterField(
            model_name="reply",
            name="reply_text",
            field=models.CharField(max_length=1000),
        ),
    ]