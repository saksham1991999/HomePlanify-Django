# Generated by Django 2.2 on 2020-08-16 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200811_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('link', models.CharField(max_length=512)),
            ],
        ),
        migrations.AlterField(
            model_name='property',
            name='bathrooms',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedrooms',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='rooms',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
