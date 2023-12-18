from django.contrib import admin

from notification_system.models import (SmtpProvider, EmailTemplate, Attachment, NotificationGroup, NotificationEvent,
                                        OutgoingMessage, Media, Contact, ContactGroup)


@admin.register(NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    list_editable = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['members']
    raw_id_fields = ['owner']
    readonly_fields = ['created_time', 'updated_time']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'owner', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    list_editable = ['is_active']
    search_fields = ['name', 'email']
    raw_id_fields = ['owner']
    readonly_fields = ['created_time', 'updated_time']


@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    list_editable = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['contacts']
    raw_id_fields = ['owner']
    readonly_fields = ['created_time', 'updated_time']


@admin.register(SmtpProvider)
class SmtpProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider_name', 'email_host', 'email_host_user', 'email_port', 'email_use_tls',
                    'email_use_ssl', 'is_active']
    list_filter = ['is_active', 'email_use_tls', 'email_use_ssl', 'created_time', 'updated_time']
    list_editable = ['is_active']
    search_fields = ['provider_name']
    filter_horizontal = ['users']
    readonly_fields = ['created_time', 'updated_time']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'subject', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    list_editable = ['is_active']
    readonly_fields = ['created_time', 'updated_time']
    raw_id_fields = ['owner']


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'notification_event', 'created_time', 'updated_time']
    list_filter = ['created_time', 'updated_time']
    raw_id_fields = ['notification_event']
    readonly_fields = ['created_time', 'updated_time']


class AttachmentInline(admin.TabularInline):
    model = Attachment


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'smtp_provider', 'template', 'is_active', 'is_sent', 'sent_time',
                    'created_time', 'updated_time']
    list_filter = ['is_active', 'sent_time', 'created_time', 'updated_time']
    list_editable = ['is_active']
    filter_horizontal = ['recipients', 'notification_groups', 'contact_groups']
    raw_id_fields = ['owner', 'smtp_provider', 'template']
    readonly_fields = ['created_time', 'updated_time']
    inlines = [AttachmentInline]


@admin.register(OutgoingMessage)
class OutgoingMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'notification_event', 'user', 'recipient', 'subject', 'status', 'outgoing_message_type',
                    'created_time', 'updated_time']
    list_filter = ['status', 'outgoing_message_type', 'created_time', 'updated_time']
    raw_id_fields = ['user', 'notification_event']
    readonly_fields = ['created_time', 'updated_time']
    search_fields = ['recipient']


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'owner', 'created_time', 'updated_time']
    list_filter = ['created_time', 'updated_time']
    raw_id_fields = ['owner']
    readonly_fields = ['created_time', 'updated_time']
