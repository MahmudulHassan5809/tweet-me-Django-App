# Generated by Django 2.1.7 on 2019-03-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0007_tweet_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='is_reply',
            field=models.BooleanField(default=False, verbose_name='Is A Reply?'),
        ),
    ]
