from django.contrib import admin
from .models import KeyPair, SignatureRecord, VerificationLog, UserActivity

@admin.register(KeyPair)
class KeyPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'private_key', 'public_key_x', 'public_key_y', 'created_at')
    search_fields = ('private_key', 'public_key_x', 'public_key_y')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    # Add custom actions
    actions = ['make_inactive']
    
    # Add fieldsets for better organization
    fieldsets = (
        ('Key Information', {
            'fields': ('private_key', 'public_key_x', 'public_key_y')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected keys as inactive"

@admin.register(SignatureRecord)
class SignatureRecordAdmin(admin.ModelAdmin):
    list_display = ('message', 'key_pair', 'timestamp', 'is_valid')
    list_filter = ('is_valid', 'timestamp')
    search_fields = ('message',)

@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'verification_result', 'verified_at')
    list_filter = ('verification_result', 'verified_at')
    search_fields = ('message',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'timestamp', 'success')
    list_filter = ('activity_type', 'success', 'timestamp')
