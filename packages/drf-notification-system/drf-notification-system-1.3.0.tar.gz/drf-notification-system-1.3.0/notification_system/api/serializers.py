import logging

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from notification_system.models import (NotificationEvent, EmailTemplate, Attachment, SmtpProvider, NotificationGroup,
                                        OutgoingMessage, Media, Contact, ContactGroup)
from notification_system.utils import get_user_common_data

User = get_user_model()

logger = logging.getLogger('notification_system')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'title', 'subject', 'content']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email']


class ContactGroupSerializer(serializers.ModelSerializer):
    contacts_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactGroup
        fields = ['id', 'name', 'contacts', 'contacts_detail']
        extra_kwargs = {
            'contacts': {'write_only': True}
        }

    def get_contacts_detail(self, obj):
        contacts = obj.contacts.filter(is_active=True)
        return ContactSerializer(instance=contacts, many=True, context=self.context).data

    def validate_contacts(self, value):
        user = self.context['request'].user
        for contact in value:
            if not contact.is_active or contact.owner != user:
                message = _("You do not have permission to access contact with id: {}.")
                raise exceptions.ValidationError(detail=message.format(contact.id))

        return value


class MinimalContactGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactGroup
        fields = ['id', 'name']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file']


class MinimalSmtpProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmtpProvider
        fields = ['id', 'provider_name']


class MinimalNotificationGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.filter(is_active=True),
                                                 required=False)

    class Meta:
        model = NotificationGroup
        fields = ['id', 'name', 'members']


class NotificationEventSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, required=False)
    template_detail = EmailTemplateSerializer(source='template', read_only=True)
    smtp_provider_detail = MinimalSmtpProviderSerializer(source='smtp_provider', read_only=True)
    notification_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=NotificationGroup.actives.all(),
                                                             required=False, write_only=True)
    notification_event_type_display = serializers.CharField(source='get_notification_event_type_display',
                                                            read_only=True)
    notification_groups_detail = MinimalNotificationGroupSerializer(source='notification_groups', many=True,
                                                                    read_only=True)
    contact_groups_detail = MinimalContactGroupSerializer(source='contact_groups', many=True, read_only=True)
    recipients = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.filter(is_active=True),
                                                    required=False, write_only=True)
    contact_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=ContactGroup.actives.all(),
                                                        required=False, write_only=True)

    class Meta:
        model = NotificationEvent
        fields = ['id', 'title', 'smtp_provider', 'smtp_provider_detail', 'template', 'template_detail', 'subject',
                  'content', 'notification_event_type', 'notification_event_type_display', 'notification_groups',
                  'notification_groups_detail', 'contact_groups_detail', 'attachments', 'recipients', 'is_sent',
                  'contact_groups', 'sent_time', 'created_time', 'updated_time']
        read_only_fields = ['is_sent', 'sent_time', 'created_time', 'updated_time']

        extra_kwargs = {
            'template': {'write_only': True, 'allow_null': True},
            'smtp_provider': {'write_only': True},
        }

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', list())
        instance = super().create(validated_data)

        attachment_list = []
        for attachment in attachments:
            attachment_list.append(Attachment(file=attachment.get('file'), notification_event=instance))

        if attachment_list:
            instance.attachments.bulk_create(attachment_list)

        return instance

    def update(self, instance, validated_data):
        attachments = validated_data.pop('attachments', list())
        instance = super().update(instance, validated_data)

        if attachments:
            instance.attachments.all().delete()

        attachment_list = []
        for attachment in attachments:
            attachment_list.append(Attachment(file=attachment.get('file'), notification_event=instance))

        if attachment_list:
            instance.attachments.bulk_create(attachment_list)

        return instance

    def validate_template(self, value):
        if value and ((not value.is_active) or (not self.context['request'].user == value.owner)):
            raise exceptions.ValidationError(detail=_("You do not have permission to access this template."))
        return value

    def validate_notification_groups(self, value):
        user = self.context['request'].user
        for notification_group in value:
            if not notification_group.is_active or notification_group.owner != user:
                message = _("You do not have permission to access notification group with id: {}.")
                raise exceptions.ValidationError(detail=message.format(notification_group.id))

        return value

    def validate_contact_groups(self, value):
        user = self.context['request'].user
        for contact_group in value:
            if not contact_group.is_active or contact_group.owner != user:
                message = _("You do not have permission to access contact groups with id: {}.")
                raise exceptions.ValidationError(detail=message.format(contact_group.id))

        return value

    def validate_smtp_provider(self, value):
        if value:
            if (not value.is_active) or (not value.users.filter(pk__in=[self.context['request'].user.id]).exists()):
                raise exceptions.ValidationError(detail=_("You do not have permission to access this smtp provider."))
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        notification_event_type = attrs.get("notification_event_type")
        smtp_provider = attrs.get("smtp_provider")

        if notification_event_type == NotificationEvent.TYPE_EMAIL and not smtp_provider:
            raise exceptions.ValidationError({"smtp_provider": _("This field is required.")})

        return attrs


class NotificationEventDetailSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, required=False)
    template_detail = EmailTemplateSerializer(source='template', read_only=True)
    smtp_provider_detail = MinimalSmtpProviderSerializer(source='smtp_provider', read_only=True)
    notification_event_type_display = serializers.CharField(source='get_notification_event_type_display',
                                                            read_only=True)
    notification_groups_detail = MinimalNotificationGroupSerializer(source='notification_groups', many=True,
                                                                    read_only=True)
    contact_groups_detail = MinimalContactGroupSerializer(source='contact_groups', many=True, read_only=True)
    total_count = serializers.IntegerField(read_only=True, default=0)
    sent_status_count = serializers.IntegerField(read_only=True, default=0)
    pending_status_count = serializers.IntegerField(read_only=True, default=0)
    failed_status_count = serializers.IntegerField(read_only=True, default=0)
    bounce_status_count = serializers.IntegerField(read_only=True, default=0)
    complaint_status_count = serializers.IntegerField(read_only=True, default=0)
    delivery_status_count = serializers.IntegerField(read_only=True, default=0)
    amazon_send_status_count = serializers.IntegerField(read_only=True, default=0)
    reject_status_count = serializers.IntegerField(read_only=True, default=0)
    open_status_count = serializers.IntegerField(read_only=True, default=0)
    click_status_count = serializers.IntegerField(read_only=True, default=0)
    rendering_failure_status_count = serializers.IntegerField(read_only=True, default=0)
    delivery_delay_status_count = serializers.IntegerField(read_only=True, default=0)
    subscription_status_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = NotificationEvent
        fields = ['id', 'title', 'smtp_provider_detail', 'template_detail', 'subject', 'content',
                  'notification_event_type', 'notification_event_type_display', 'notification_groups_detail',
                  'contact_groups_detail', 'attachments', 'is_sent', 'sent_time', 'created_time', 'updated_time',
                  'total_count', 'sent_status_count', 'pending_status_count', 'failed_status_count',
                  'bounce_status_count', 'complaint_status_count', 'delivery_status_count', 'amazon_send_status_count',
                  'reject_status_count', 'open_status_count', 'click_status_count', 'rendering_failure_status_count',
                  'delivery_delay_status_count', 'subscription_status_count']


class MinimalNotificationEventSerializer(serializers.ModelSerializer):
    template_detail = EmailTemplateSerializer(source='template', read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    notification_event_type_display = serializers.CharField(source='get_notification_event_type_display',
                                                            read_only=True)

    class Meta:
        model = NotificationEvent
        fields = ['id', 'title', 'subject', 'content', 'notification_event_type', 'notification_event_type_display',
                  'template_detail', 'attachments', 'is_sent', 'sent_time', 'created_time', 'updated_time']
        read_only_fields = ['is_sent', 'sent_time', 'created_time', 'updated_time']


class OutgoingMessageSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    outgoing_message_type_display = serializers.CharField(source="get_outgoing_message_type_display", read_only=True)
    notification_event_detail = MinimalNotificationEventSerializer(source='notification_event', read_only=True)
    rendered_content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OutgoingMessage
        fields = ['id', 'notification_event_detail', 'recipient', 'subject', 'status', 'status_display', 'content',
                  'rendered_content', 'outgoing_message_type', 'outgoing_message_type_display', 'created_time',
                  'updated_time']

    def get_rendered_content(self, obj):
        template_instance = Template(template_string=obj.content or '')
        context = get_user_common_data(user=obj.user)
        context_instance = Context(dict_=context)
        content = template_instance.render(context=context_instance)
        return content


class OutgoingMessageNotificationSerializer(serializers.Serializer):
    Type = serializers.CharField(required=False)
    notificationType = serializers.CharField(required=False)
    mail = serializers.DictField(write_only=True, required=False)
    outgoing_message_id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        flag_check_condition = True

        if attrs.get('Type') == "SubscriptionConfirmation":
            msg = _("Amazon SubscriptionConfirmation webhook received. data: {}".format(self.context['request'].data))
            logger.info(msg=msg)
            raise exceptions.ParseError(_("The payload is not valid."))

        for mail_header in attrs.get('mail', dict()).get('headers', []):
            name = mail_header.get('name')
            value = mail_header.get('value')
            if (name == 'outgoing_message_id') and value:
                if value.isdigit():
                    attrs['outgoing_message_id'] = value
                    flag_check_condition = False

        if flag_check_condition:
            raise exceptions.ParseError(_("The payload is not valid."))

        return attrs
