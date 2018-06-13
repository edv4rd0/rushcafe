from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form, ModelChoiceField, ModelForm
from django.forms.widgets import NumberInput, PasswordInput, TextInput

from rushcafe.models import MenuCategory, MenuItem


class MenuCategoryForm(ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']


class DeleteForm(Form):
    deleted = forms.BooleanField(required=True)

    def is_valid(self):
        """We will invalidate data if it's not setting the delete flag.
        This simplifies the view logic."""
        valid = super().is_valid()

        if valid:
            if self.cleaned_data['deleted'] is True:
                return True
        return valid


class MenuItemForm(ModelForm):
    category = ModelChoiceField(
        queryset=MenuCategory.objects.filter(deleted=False)
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'price']

    name = forms.CharField(widget=TextInput(attrs={
        'class': 'validate',
        'placeholder': 'Name'
    }))
    price = forms.DecimalField(widget=NumberInput(attrs={
        'class': 'validate',
        'placeholder': 9.99
    }))


class RushCafeAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={
            'class': 'validate',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=PasswordInput(
        attrs={'placeholder': 'Password'}
    ))
