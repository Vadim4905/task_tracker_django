from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done' ,'Done'),
    ]
    PRIORITY_CHOICES=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'HIgh'),
        ('critical', 'Critical'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=31, choices=STATUS_CHOICES,default='todo')
    priority = models.CharField(max_length=31, choices=PRIORITY_CHOICES,default='medium')
    dude_date = models.DateTimeField(null=True,blank=True)
    creator = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='tasks')
    is_publick = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='comments_media/',blank=True,null=True)
    def __str__(self):
        return self.content
    
    
class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.comment} comment'


    class Meta:
        unique_together = ('comment', 'user')  
