from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.forms.widgets import PasswordInput, TextInput, NumberInput


from rushcafe.models import MenuCategory, MenuItem

class MenuCategoryForm(ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']


class MenuItemForm(ModelForm):
    category = ModelChoiceField(queryset=MenuCategory.objects.all())
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'price']

    name = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder': 'Name'}))
    price = forms.DecimalField(widget=NumberInput(attrs={'class':'validate', 'placeholder': 9.99}))


class RushCafeAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
