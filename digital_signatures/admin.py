from django.contrib import admin
from .models import KeyPair, SignatureRecord, VerificationLog, UserActivity, DocumentMetadata, SignatureStats, AuditLog

@admin.register(KeyPair)
class KeyPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_key_x', 'public_key_y', 'created_at')
    search_fields = ('public_key_x', 'public_key_y')

@admin.register(SignatureRecord)
class SignatureRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'signature_r', 'signature_s', 'is_valid', 'timestamp')
    list_filter = ('is_valid', 'timestamp')

@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'verification_result', 'verified_at')
    list_filter = ('verification_result', 'verified_at')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity_type', 'success', 'timestamp')
    list_filter = ('activity_type', 'success', 'timestamp')

@admin.register(DocumentMetadata)
class DocumentMetadataAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'upload_date')
    search_fields = ('file_name', 'hash_value')
    list_filter = ('file_type', 'upload_date')

@admin.register(SignatureStats)
class SignatureStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_signatures', 'successful_verifications', 'failed_verifications')
    list_filter = ('date',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'timestamp', 'ip_address', 'status')
    list_filter = ('action', 'status', 'timestamp')
    search_fields = ('ip_address', 'user_agent')
