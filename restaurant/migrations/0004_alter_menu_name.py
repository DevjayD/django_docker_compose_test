# Generated by Django 3.2.6 on 2021-08-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0003_alter_isvoted_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]