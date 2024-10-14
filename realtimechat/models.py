from django.db import models
from django.contrib.auth.models import User
import uuid
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=200, unique=True)
    users_online = models.ManyToManyField(User,related_name='online_in_groups',blank=True)
    
    def __str__(self):
        return self.group_name
    
class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE,related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return f'{self.author.username} : {self.body}'
    class Meta:
        ordering =['-created']
