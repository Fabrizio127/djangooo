# Generated by Django 3.2.3 on 2021-05-20 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicpro', '0003_marca_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='descuento',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(default=0, null=True),
        ),
    ]