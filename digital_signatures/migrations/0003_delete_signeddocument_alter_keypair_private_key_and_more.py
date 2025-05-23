# Generated by Django 5.0.8 on 2024-10-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital_signatures', '0002_signeddocument_alter_keypair_private_key_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SignedDocument',
        ),
        migrations.AlterField(
            model_name='keypair',
            name='private_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='keypair',
            name='public_key_x',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='keypair',
            name='public_key_y',
            field=models.CharField(max_length=255),
        ),
    ]
