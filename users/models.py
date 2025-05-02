from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        return self.display_name or self.user.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/image.svg')
        return avatar