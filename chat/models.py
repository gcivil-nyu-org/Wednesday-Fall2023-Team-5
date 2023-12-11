from django.db import models  # noqa
from django.contrib.auth.models import User
from datetime import datetime


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
    receiving_image_url = models.CharField(default="")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.thread.updated = datetime.utcnow()
            self.thread.save()
        return super(ChatMessage, self).save(*args, **kwargs)
