from django.contrib import admin
from .models import Hood, Location,Post, User

# Register your models here.
admin.site.register(User)
admin.site.register(Hood)
admin.site.register(Location)
admin.site.register(Post)
