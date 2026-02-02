from django.db import models
from django.contrib.auth.models import User
from tracking.models import SubPartType


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('PIC', 'Person In Charge'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    sub_part_type = models.ForeignKey(
        SubPartType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
