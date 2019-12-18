from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins

from invitations.models import Invitation
from invitations.serializers import InvitationSerializer


class InvitationListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    APIView that provides two actions for authenticated users;
    `list` invitations with pagination, `create` an invitation
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvitationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView that provides actions for authenticated users;
    `get`, `patch` and `delete` an existing invitation.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'id'
