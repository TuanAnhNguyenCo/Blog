# Generated by Django 4.0.3 on 2022-04-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questions',
            options={'ordering': ['-create_at']},
        ),
        migrations.AddField(
            model_name='questions',
            name='fullname',
            field=models.CharField(default='member', max_length=100),
        ),
    ]