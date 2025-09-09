from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder': 'John Doe'})
        self.fields['email'].widget.attrs.update({'placeholder': 'JohnDoe@example.com'})
        self.fields['password1'].widget.attrs.update({'placeholder': '********'})
        self.fields['password2'].widget.attrs.update({'placeholder': '********'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "is_active", "is_staff", "is_superuser") # add all fields here