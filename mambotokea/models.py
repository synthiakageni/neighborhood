from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    profile_pic = CloudinaryField(null=True, default='user.png')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Hood(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    occupants = models.ManyToManyField(User, related_name='occupants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    fire_department = models.IntegerField(null=True)
    hospital_contact = models.IntegerField(null=True)
    security_department = models.IntegerField(null=True)
    biashara = models.ManyToManyField('Business', related_name='biashara', blank=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    neighborhood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    contact = models.IntegerField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name 


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
       

    def __str__(self):
        return self.body[0:50]

