# Generated by Django 3.2.3 on 2021-05-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pareri',
            fields=[
                ('id_feedback', models.AutoField(primary_key=True, serialize=False)),
                ('student', models.IntegerField()),
                ('profesor', models.IntegerField()),
                ('nota', models.IntegerField()),
                ('mesaj', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'pareri',
                'managed': False,
            },
        ),
    ]
