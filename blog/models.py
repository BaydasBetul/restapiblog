from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now

# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)

    Category = (
        ("1", "Travel"),
        ("2", "Programming"),
        ("3", "Beauty"),
        ("4", "Health"),
        ("5", "Spor"),
        ("6", "Other"),
    )

    Status = (
        ("D", "Draft"),
        ("V", "View"),
    )

    category = models.CharField(max_length=20, choices=Category, default='6')
    statuse = models.CharField(max_length=6, choices=Status, default='D')

    def __str__(self):
        return f"{self.user} {self.title} {self.content}"


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    dateTime = models.DateTimeField(default=now)  # auto_now_add=True

    def __str__(self):
        return f'{self.user} {self.content}'


class Like(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.blog}'


class BlogView(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.blog}'
