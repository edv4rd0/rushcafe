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

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    class Meta:
        ordering = ['-name']

    name = models.CharField('Name',
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

    def __str__(self):
        return self.name


