from user.models import Profile
from django.db import models




class Category(models.Model):  
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Series(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="series/")
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.price}"