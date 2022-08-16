from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
import string

# Create your models here.

class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.slug = '{slug}-{auto_rand}'.format(slug=slugify(self.title),auto_rand=''.join(random.choice(letters) for i in range(10)))
        super(Notes, self).save(*args, **kwargs)