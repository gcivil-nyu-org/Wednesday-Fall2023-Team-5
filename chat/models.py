from django.db import models  # noqa
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models import Q

from user_profile.models import UserImages


# Create your models here.


class Thread(models.Model):
    first_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chatroom_first_user",
    )
    second_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chatroom_second_user",
    )
    updated = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["first_user", "second_user"]


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chat_message",
    )
    sending_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sending_image_url = models.CharField(default="")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.thread.updated = datetime.utcnow()
            self.thread.save()
            sender_image_url = ""
            sender_image = UserImages.objects.filter(Q(user_profile_id=self.thread.first_user.id))
            sender_instances = [UserImages(**item) for item in sender_image.values()]
            if len(sender_instances) > 0:
                self.sending_image_url = sender_instances[0].get_absolute_url()
            else:
                self.sending_image_url = sender_image_url
        return super(ChatMessage, self).save(*args, **kwargs)
