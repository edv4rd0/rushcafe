from django.contrib.sessions.models import Session
from django.db import models


class MenuCategory(models.Model):
    """Data model for a category on the menu.
    XXX: unique constraint on name with user interface to support this.
         This includes handling adding a new item with the same name
         as a 'deleted' category"""
    class Meta:
        ordering = ['-name']

    name = models.CharField(
        'Name',
        blank=False,
        null=False,
        help_text='Category name',
        max_length=20,
    )
    deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Data model for an item on the menu.
    XXX: unique constraint on name with user interface to support this.
         This includes handling adding a new item with the same name
         as the 'deleted' menu item"""
    class Meta:
        ordering = ['-name']

    name = models.CharField(
        'Name',
        blank=False,
        null=False,
        help_text='Category name',
        max_length=20,
    )
    category = models.ForeignKey(
        MenuCategory,
        related_name='menu_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False
    )
    deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    """Used to store messages sent and received.

    This can be changed to have references to what
    the bot message is replying to, rather than
    relying on timestamps.

    Just getting basic functionality in here at this stage"""
    user_session = models.ForeignKey(
        Session,
        related_name='chat_messages',
        on_delete=models.CASCADE,
    )
    message = models.CharField(
        blank=True,
        max_length=300,
    )
    time_stamp = models.DateTimeField(auto_now=True)
    is_bot = models.BooleanField(default=False)
