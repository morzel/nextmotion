from rest_framework import serializers
from invitations.models import Invitation
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail


def send_invitation_mail(from_email, to_email):
    """
    Send an email to `email
    """
    send_mail(
        'Invitation',
        from_email + ' has sent you an invitation.',
        from_email,
        [to_email],
    )


class InvitationSerializer(serializers.ModelSerializer):
    createdTime = serializers.DateTimeField(source='created_time', read_only=True)
    seconds = serializers.SerializerMethodField()
    creatorEmail = serializers.SerializerMethodField()
    creatorFullname = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ('id', 'createdTime', 'seconds', 'email', 'used', 'creatorEmail', 'creatorFullname',)
        read_only_fields = ('id',)

    def get_seconds(self, obj):
        return (timezone.now() - obj.created_time).seconds

    def get_creatorEmail(self, obj):
        return obj.creator.email

    def get_creatorFullname(self, obj):
        return obj.creator.first_name + ' ' + obj.creator.last_name

    def create(self, validated_data):
        """
        Set the creator for new invitation created and send an email
        """
        cur_user = self.context.get('request').user
        new_invitation = Invitation.objects.create(creator=cur_user, **validated_data)
        send_invitation_mail(cur_user.email, new_invitation.email)

        return new_invitation

    def update(self, instance, validated_data):
        """
        When updating an existing invitation, if email has been changed send an email
        """
        cur_user = self.context.get('request').user
        prev_email = instance.email
        super(InvitationSerializer, self).update(instance, validated_data)

        if prev_email != validated_data['email']:
            send_invitation_mail(cur_user.email, validated_data['email'])

        return instance
