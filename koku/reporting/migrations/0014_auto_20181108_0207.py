# Generated by Django 2.1.2 on 2018-11-08 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0013_auto_20181107_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocpusagelineitemdailysummary',
            name='pod_charge_cpu_cores',
            field=models.DecimalField(decimal_places=6, max_digits=24, null=True),
        ),
        migrations.AddField(
            model_name='ocpusagelineitemdailysummary',
            name='pod_charge_memory_gigabytes',
            field=models.DecimalField(decimal_places=6, max_digits=24, null=True),
        ),
    ]