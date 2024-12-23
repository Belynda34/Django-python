# Generated by Django 4.2.16 on 2024-10-22 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ems1', '0002_alter_event_enddate_alter_event_startdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('services_offered', models.TextField(max_length=255)),
                ('phone_numer', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendors', to='ems1.event')),
            ],
        ),
    ]
