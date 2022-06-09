from django.db import models
from django.contrib.auth.models import User
from members.models import Powerteam


class Questions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    powerteam = models.ForeignKey(Powerteam,on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=1000,null=False,blank=False)
    description = models.TextField(null=False,blank=False)
    images = models.ImageField(null = True,blank = True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']
    
    def __str__(self) -> str:
        return self.title

class Answers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    images = models.ImageField(null = True,blank = True)
    answer = models.TextField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.answer

class Tags(models.Model):
    question = models.ManyToManyField(Questions,through="Tagship")
    tag = models.CharField(max_length=100,null=False,blank=False)

class Tagship(models.Model):
    tag = models.ForeignKey(Tags,on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)




