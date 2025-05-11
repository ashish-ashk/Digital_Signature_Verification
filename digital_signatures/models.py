from django.db import models
from django.utils import timezone

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