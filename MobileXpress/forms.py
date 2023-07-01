from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, PasswordInput, Form, ModelForm, ModelChoiceField, inlineformset_factory, \
    ImageField

from .models import *


class RegistrationForm(Form):
    username = CharField(max_length=150)
    password = CharField(widget=PasswordInput)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField()
    profile_picture = ImageField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')
        )
        custom_user = CustomUser.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            profile_picture=self.cleaned_data.get('profile_picture')
        )
        return custom_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control-file'


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "cart", "date_created", "total_amount", "order_status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class MyPhoneColorQuantityForm(ModelForm):
    class Meta:
        model = PhoneColorQuantity
        exclude = ["phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3 w-50'


class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


PhoneColorQuantityFormSet = inlineformset_factory(
    Phone,
    PhoneColorQuantity,
    fields=('color', 'quantity'),
    extra=5,
    can_delete=False,
    form=MyPhoneColorQuantityForm,
)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = ["order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
