# Generated by Django 5.1 on 2024-09-29 20:01

import django.db.models.deletion
import inventory_items.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_items', '0018_alter_itemmodel_box_alter_itemmodel_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodel',
            name='box',
            field=models.ForeignKey(blank=True, default=inventory_items.models.BoxModel.get_default_box, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory_items.boxmodel', verbose_name='Упаковка'),
        ),
    ]