from django.test import TestCase
from django.test import TestCase
from .models import User, Hood, Post, Business
from django.contrib.auth.models import User


# Create your tests here.

class UserTestClass(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.user = User(username='martin')
        self.user.save()
        self.profile = User(id=1,user=self.user,profile_pic='download.jpeg',bio='My name is Martin', location='Ndarugo', hood_name='person')
        self.profile.save_user_profile()
    def tearDown(self):
        User.objects.all().delete()
        User.objects.all().delete()
        Hood.objects.all().delete()
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.profile, User))
    def test_save_method(self):
        self.profile.save_user_profile()
        profile = User.objects.all()
        self.assertTrue(len(profile) > 0)


