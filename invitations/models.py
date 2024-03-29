from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    email = models.EmailField()
    used = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_invitations',
        on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "invitation to " + self.email