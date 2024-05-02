from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ConsultantUser, GestionnaireUser, AdminUser
from multiupload.fields import MultiFileField


class RegularUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ConsultantUser
        fields = ('username', 'email')


class PremiumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = GestionnaireUser
        fields = ('username', 'email')


class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AdminUser
        fields = ('username', 'email')



class UploadFileForm(forms.Form):
    files = MultiFileField(max_num=5, max_file_size=1024*1024*5)