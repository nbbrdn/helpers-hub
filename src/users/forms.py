from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import HubUser


class HubUserCreationForm(UserCreationForm):
    class Meta:
        model = HubUser
        fields = ("email",)


class HubUserChangeForm(UserChangeForm):
    class Meta:
        model = HubUser
        fields = ("email",)
