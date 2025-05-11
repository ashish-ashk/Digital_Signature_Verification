from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class KeyPair(models.Model):
    private_key = models.CharField(max_length=255)
    public_key_x = models.CharField(max_length=255)
    public_key_y = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KeyPair {self.id}"

class SignatureRecord(models.Model):
    message = models.TextField()
    signature_r = models.CharField(max_length=255)
    signature_s = models.CharField(max_length=255)
    key_pair = models.ForeignKey(KeyPair, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.localtime)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Signature for message: {self.message[:30]}..."

class VerificationLog(models.Model):
    message = models.TextField()
    public_key_x = models.CharField(max_length=255)
    public_key_y = models.CharField(max_length=255)
    signature_r = models.CharField(max_length=255)
    signature_s = models.CharField(max_length=255)
    verified_at = models.DateTimeField(auto_now_add=True)
    verification_result = models.BooleanField()

    def __str__(self):
        return f"Verification at {self.verified_at}: {'Success' if self.verification_result else 'Failed'}"

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('GEN', 'Key Generation'),
        ('SIGN', 'Message Signing'),
        ('VER', 'Signature Verification')
    ]
    activity_type = models.CharField(max_length=4, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.get_activity_type_display()} at {self.timestamp}"

class DocumentMetadata(models.Model):
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    hash_value = models.CharField(max_length=64)  # Store SHA-256 hash
    upload_date = models.DateTimeField(auto_now_add=True)
    signature_record = models.ForeignKey(SignatureRecord, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-upload_date']

class SignatureStats(models.Model):
    total_signatures = models.IntegerField(default=0)
    successful_verifications = models.IntegerField(default=0)
    failed_verifications = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    average_processing_time = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = 'Signature Statistics'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_documents_signed = models.IntegerField(default=0)
    last_signature_date = models.DateTimeField(null=True, blank=True)
    trusted_public_keys = models.ManyToManyField(KeyPair)
    default_signature_type = models.CharField(
        max_length=20,
        choices=[
            ('QUICK', 'Quick Sign'),
            ('DETAILED', 'Detailed Sign')
        ],
        default='QUICK'
    )

class AuditLog(models.Model):
    ACTIONS = [
        ('CREATE', 'Create Key Pair'),
        ('SIGN', 'Sign Document'),
        ('VERIFY', 'Verify Signature'),
        ('DELETE', 'Delete Key Pair'),
        ('EXPORT', 'Export Keys'),
        ('ACCESS', 'Access Document')
    ]
    
    action = models.CharField(max_length=10, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    status = models.BooleanField(default=True)
    details = models.JSONField()

class SignatureBatch(models.Model):
    batch_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PROCESSING', 'Processing'),
            ('COMPLETED', 'Completed'),
            ('FAILED', 'Failed')
        ],
        default='PENDING'
    )
    total_documents = models.IntegerField(default=0)
    processed_documents = models.IntegerField(default=0)
    key_pair = models.ForeignKey(KeyPair, on_delete=models.PROTECT)