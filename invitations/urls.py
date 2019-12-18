from django.urls import path
from invitations.views import InvitationListAPIView, InvitationDetailAPIView

app_name = "invitations"
urlpatterns = [
    path('invitations/', InvitationListAPIView.as_view(), name='invitations_list'),
    path('invitations/<slug:id>', InvitationDetailAPIView.as_view(), name='invitations_detail'),
]