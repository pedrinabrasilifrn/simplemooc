# Generated by Django 3.2.9 on 2022-03-25 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_enrollment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Cancelado')], default=1, verbose_name='Situação'),
        ),
    ]
