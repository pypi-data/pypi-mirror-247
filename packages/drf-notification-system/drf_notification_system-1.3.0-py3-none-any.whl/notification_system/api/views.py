from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from notification_system.api.serializers import (NotificationEventSerializer, EmailTemplateSerializer,
                                                 OutgoingMessageSerializer, MinimalNotificationGroupSerializer,
                                                 MinimalSmtpProviderSerializer, OutgoingMessageNotificationSerializer,
                                                 MediaSerializer, NotificationEventDetailSerializer, ContactSerializer,
                                                 ContactGroupSerializer)
from notification_system.models import (NotificationEvent, EmailTemplate, OutgoingMessage, NotificationGroup,
                                        SmtpProvider, Media, Contact, ContactGroup)
from notification_system.notification_delivery import broadcast_event_messages_to_recipients
from notification_system.paginations import CustomLimitOffsetPagination
from notification_system.parsers import PlainTextParser
from notification_system.permissions import CustomDjangoModelPermissions
from notification_system.tasks import update_outgoing_message_status


class NotificationEventViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    """
    A ViewSet for viewing Notification Event.
    """
    queryset = NotificationEvent.actives.all()
    serializer_class = NotificationEventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id']
    filter_fields = ['notification_groups', 'recipients', 'notification_event_type', 'is_sent', 'contact_groups']

    def get_queryset(self):
        filter_params = {
            'broadcast_message': {'is_sent': False},
        }.get(self.action, dict())

        annotate_params = {
            'retrieve': {
                'total_count': Count('outgoing_messages'),
                'sent_status_count': Count('outgoing_messages',
                                           filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_SENT)),
                'pending_status_count': Count('outgoing_messages',
                                              filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_PENDING)),
                'failed_status_count': Count('outgoing_messages',
                                             filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_FAILED)),
                'bounce_status_count': Count('outgoing_messages',
                                             filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_BOUNCE)),
                'complaint_status_count':
                    Count('outgoing_messages',
                          filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_COMPLAINT)),

                'delivery_status_count':
                    Count('outgoing_messages',
                          filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_DELIVERY)),

                'amazon_send_status_count':
                    Count('outgoing_messages', filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_SEND)),

                'reject_status_count': Count('outgoing_messages',
                                             filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_REJECT)),

                'open_status_count': Count('outgoing_messages',
                                           filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_OPEN)),

                'click_status_count': Count('outgoing_messages',
                                            filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_CLICK)),

                'rendering_failure_status_count':
                    Count('outgoing_messages',
                          filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_RENDERING_FAILURE)),

                'delivery_delay_status_count':
                    Count('outgoing_messages',
                          filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_DELIVERY_DELAY)),

                'subscription_status_count':
                    Count('outgoing_messages',
                          filter=Q(outgoing_messages__status=OutgoingMessage.STATUS_AMAZON_SUBSCRIPTION)),
            }
        }.get(self.action, dict())

        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('attachments', 'notification_groups__members', 'notification_groups',
                                             'contact_groups')
        queryset = queryset.prefetch_related('recipients').select_related('smtp_provider', 'template')
        return queryset.filter(owner=self.request.user, **filter_params).annotate(**annotate_params)

    def get_serializer_class(self):
        return {
            'retrieve': NotificationEventDetailSerializer,

        }.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'], url_path="broadcast-message")
    def broadcast_message(self, request, pk=None):
        instance = self.get_object()
        broadcast_event_messages_to_recipients(event_message_id=instance.id)
        instance.is_sent = True
        instance.sent_time = timezone.now()
        instance.save(update_fields=['is_sent', 'sent_time'])

        return Response(status=200)


class EmailTemplateViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    A ViewSet for viewing Notification Event.
    """
    queryset = EmailTemplate.actives.select_related('owner').all()
    serializer_class = EmailTemplateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    A ViewSet for viewing Contacts.
    """
    queryset = Contact.actives.select_related('owner').all()
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactGroupViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    A ViewSet for viewing Contact groups.
    """
    queryset = ContactGroup.actives.all()
    serializer_class = ContactGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OutgoingMessageViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    A ViewSet for viewing outgoing message.
    """
    queryset = OutgoingMessage.objects.all()
    serializer_class = OutgoingMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id']
    filter_fields = ['outgoing_message_type', 'status', 'notification_event']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('notification_event__attachments')
        queryset = queryset.select_related('user', 'notification_event', 'notification_event__template')
        return queryset.filter(Q(user=self.request.user) | Q(recipient=self.request.user.email)).distinct()


class NotificationGroupViewSet(mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """
    A ViewSet for viewing notification group.
    """
    queryset = NotificationGroup.actives.select_related('owner').all()
    serializer_class = MinimalNotificationGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SmtpProviderViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    A ViewSet for viewing smtp provider.
    """
    queryset = SmtpProvider.actives.prefetch_related('users').all()
    serializer_class = MinimalSmtpProviderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(users__id__in=[self.request.user.id]).distinct()


class MedialViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    A ViewSet for viewing user uploaded media.
    """
    queryset = Media.objects.select_related('owner').all()
    serializer_class = MediaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OutgoingMessageNotificationAPIView(APIView):
    parser_classes = [PlainTextParser, JSONParser]

    def post(self, request):
        serializer = OutgoingMessageNotificationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        kwargs = {
            'outgoing_message_id': serializer.data.get('outgoing_message_id'),
            'status': serializer.data.get('notificationType')
        }
        update_outgoing_message_status_queue_name = getattr(settings, 'UPDATE_OUTGOING_MESSAGE_STATUS_QUEUE_NAME',
                                                            'update_outgoing_message_status')
        update_outgoing_message_status.apply_async(kwargs=kwargs, queue=update_outgoing_message_status_queue_name)
        return Response(serializer.data)
