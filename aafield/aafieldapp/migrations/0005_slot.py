# Generated by Django 2.2.6 on 2020-04-10 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aafieldapp', '0004_auto_20200409_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start_Time', models.TimeField()),
                ('End_Time', models.TimeField()),
                ('Slot_Name', models.CharField(blank=True, default=' ', max_length=50, null=True)),
                ('Order', models.IntegerField(blank=True, null=True)),
                ('Park_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aafieldapp.Parks')),
                ('Property_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aafieldapp.Park_Properties')),
            ],
        ),
    ]
