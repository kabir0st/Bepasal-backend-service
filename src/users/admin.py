from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Document, VerificationCode


class VerificationCodeAdmin(ModelAdmin):
    list_display = (
        'email',
        'code',
        'is_email_sent',
        'created_at',
    )
    search_fields = ('email', 'code')
    list_filter = ('is_email_sent', 'created_at')
    readonly_fields = ('hash', 'created_at')


class DocumentAdmin(ModelAdmin):
    list_display = ('uuid', 'name', 'model', 'status', 'created_at')
    search_fields = ('name', 'model', 'uuid')
    list_filter = ('status', 'created_at')
    readonly_fields = ('uuid', 'created_at')


admin.site.register(VerificationCode, VerificationCodeAdmin)
admin.site.register(Document, DocumentAdmin)
