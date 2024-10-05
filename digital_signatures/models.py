from django.db import models

class KeyPair(models.Model):
    private_key = models.CharField(max_length=255)
    public_key_x = models.CharField(max_length=255)
    public_key_y = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KeyPair {self.id}"