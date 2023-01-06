# Generated by Django 3.2.16 on 2022-12-21 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20221221_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='format',
            field=models.CharField(choices=[('h5', 'H5'), ('h5r', 'H5R'), ('pkl', 'Pickle')], max_length=50, verbose_name='Format'),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]