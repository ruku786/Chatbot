from django.db import models

# Create your models here.
class UserData(models.Model):
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=40)
    user_type = models.CharField( max_length=10)
    
    def __str__(self):
        return self.user_id


class Chat(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    question_ans = models.BooleanField(default = True)
    answer = models.CharField(max_length=255, blank= True, null = True)
    def __str__(self):
        return self.user_id
