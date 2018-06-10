from django.db import models


class MenuCategory(models.Model):
    class Meta:
        ordering = ['-name']
    
    name = models.CharField('Name',
        blank=False,
        null=False,
        help_text='Category name',
        max_length=20,
    )


class MenuItem(models.Model):
    class Meta:
        ordering = ['-name']

    name = models.CharField('Name',
        blank=False,
        null=False,
        help_text='Category name',
        max_length=20,
    )
    models.ForeignKey(
        MenuCategory,
        related_name='menu_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False
    )
