# Generated by Django 5.0.8 on 2025-05-11 09:25

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital_signatures', '0006_alter_signaturerecord_timestamp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('CREATE', 'Create Key Pair'), ('SIGN', 'Sign Document'), ('VERIFY', 'Verify Signature'), ('DELETE', 'Delete Key Pair'), ('EXPORT', 'Export Keys'), ('ACCESS', 'Access Document')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('details', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='SignatureStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_signatures', models.IntegerField(default=0)),
                ('successful_verifications', models.IntegerField(default=0)),
                ('failed_verifications', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('average_processing_time', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name_plural': 'Signature Statistics',
            },
        ),
        migrations.CreateModel(
            name='DocumentMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=50)),
                ('file_size', models.IntegerField()),
                ('hash_value', models.CharField(max_length=64)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('signature_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='digital_signatures.signaturerecord')),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
        migrations.CreateModel(
            name='SignatureBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('total_documents', models.IntegerField(default=0)),
                ('processed_documents', models.IntegerField(default=0)),
                ('key_pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='digital_signatures.keypair')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_documents_signed', models.IntegerField(default=0)),
                ('last_signature_date', models.DateTimeField(blank=True, null=True)),
                ('default_signature_type', models.CharField(choices=[('QUICK', 'Quick Sign'), ('DETAILED', 'Detailed Sign')], default='QUICK', max_length=20)),
                ('trusted_public_keys', models.ManyToManyField(to='digital_signatures.keypair')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
