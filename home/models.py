from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
import json 
from django.utils import timezone
# Create your models here.
User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    fullname=models.TextField()
    phone=models.TextField()
    role=models.TextField(blank=True)
    field=models.TextField()
    birthdate=models.TextField(blank=True)
    usermode=models.IntegerField()
    information = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    
    
    def __str__(self):
        return self.user.username
    
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    que = models.TextField()
    answers = models.TextField()
    count = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user
    chat_data = models.TextField()  # Store chat entries as JSON serialized data
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_time = models.TimeField(null=True)

    def __str__(self):
        return f"Conversation with {self.user.username}"

    def get_chat_entries(self):
        try:
            return json.loads(self.chat_data)
        except json.JSONDecodeError:
            return []

    def add_chat_entry(self, entry):
        chat_data = self.get_chat_entries()
        chat_data.append(entry)
        self.chat_data = json.dumps(chat_data)
        self.save()
        
    def save(self, *args, **kwargs):
        # Set the created_time to the current time before saving
        if not self.created_time:
            self.created_time = timezone.now().time()
        super(Conversation, self).save(*args, **kwargs)    
