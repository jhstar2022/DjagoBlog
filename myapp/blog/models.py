from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

