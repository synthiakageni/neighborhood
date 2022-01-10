from django.forms import ModelForm
from.models import Hood, User, Business
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


        
class HoodForm(ModelForm):
    class Meta:
        model = Hood
        fields = '__all__'
        exclude = ['host', 'occupants', 'biashara']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','username','email','profile_pic','bio']


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'email','contact']
