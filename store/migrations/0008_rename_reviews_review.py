# Generated by Django 4.2.6 on 2023-10-20 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_orderitem_product_and_adding_reviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]
