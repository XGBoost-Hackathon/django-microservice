# Generated by Django 4.1.3 on 2023-07-13 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadFiles', '0003_rename_files_uploadfiles_file_alter_uploadfiles_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfiles',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]