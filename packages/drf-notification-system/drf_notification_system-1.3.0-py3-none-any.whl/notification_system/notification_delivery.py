from django.conf import settings

from notification_system.common.notification_handler import EmailNotificationHandler, NotificationHandler
from notification_system.models import NotificationEvent
from notification_system.tasks import notification_system_send_internal_message
from notification_system.utils import get_user_common_data


def broadcast_event_messages_to_recipients(event_message_id):
    notification_event = NotificationEvent.objects.prefetch_related('notification_groups__members', 'attachments')
    notification_event = notification_event.prefetch_related('notification_groups')
    notification_event = notification_event.select_related('smtp_provider', 'owner', 'template')
    notification_event = notification_event.get(id=event_message_id)

    if notification_event.notification_event_type == NotificationEvent.TYPE_EMAIL:
        subject = notification_event.get_subject()
        html_content = notification_event.get_content()
        recipients = notification_event.get_recipients()
        contacts = notification_event.get_contacts()
        email_from = notification_event.smtp_provider.email_from
        smtp_config = notification_event.smtp_provider.get_smtp_config()
        if getattr(settings, 'USE_S3_MEDIA', False):
            attachments = list(notification_event.attachments.values_list('id', flat=True))
        else:
            attachments = [attachment.file.path for attachment in notification_event.attachments.all()]

        for user in recipients:
            context = get_user_common_data(user=user)
            notification_handler = EmailNotificationHandler(subject=subject, recipient=user.email,
                                                            email_from=email_from,
                                                            context=context, content=html_content, user_id=user.id,
                                                            smtp_config=smtp_config, attachments=attachments,
                                                            notification_event=notification_event.id)
            notification_handler.send()

        for contact in contacts:
            email = contact.get('email')
            context = {
                'email': email,
                'username': email,
                'first_name': contact.get('contact_name'),
            }
            notification_handler = EmailNotificationHandler(subject=subject, recipient=email,
                                                            email_from=email_from, context=context,
                                                            content=html_content, smtp_config=smtp_config,
                                                            attachments=attachments,
                                                            notification_event=notification_event.id)
            notification_handler.send()

    else:
        queue_name = NotificationHandler.INTERNAL_MESSAGE_NOTIFICATION_QUEUE_NAME
        notification_system_send_internal_message.apply_async(args=(notification_event.pk,), queue=queue_name)

    return True
