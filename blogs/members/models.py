from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Hồ sơ của các thành viên
class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneNumber = models.CharField(null=False,blank=False,max_length=20)
    images = models.ImageField(null = True)
    likes = models.IntegerField(default=0)
    address = models.CharField(max_length=200,null=False,blank=False)
    university = models.CharField(max_length=100,null=False,blank = False)
    gen = models.DecimalField(max_digits=5,decimal_places=1)
    fullname = models.CharField(max_length=100,null=False,blank=False,default='member')
    PTPTgroup = models.IntegerField(default=0)

    def __str__(self) -> str:
        return "%s profile"%self.user

# Các dự án thành viên tham gia
class projects(models.Model):
    user = models.ManyToManyField(User,through="Projectship")
    name = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField(null=False,blank=False)
    status = models.BooleanField(default=False)

# Mô hình trung gian tạo mối quan hệ giữa user và projects
class Projectship(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    projects = models.ForeignKey(projects,on_delete=models.CASCADE)

# Đánh giá dự án cho các thành viên
class ProjectEvaluation(models.Model):
    projects = models.ForeignKey(projects,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    evaluation = models.TextField(null=False,blank=False)

# Khó khăn của các thành viên
class diffculty(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False,blank=False)
    name = models.TextField(null=False,blank=False)
    solved = models.BooleanField(default=False)

# Ban mà thành viên đó đang ở
class Ban(models.Model):
    user = models.ManyToManyField(User,through="Banship")
    name = models.CharField(max_length=100,null=False,blank=False)
    headOfBan = models.CharField(max_length=100,null=False,blank=False)

# Mô hình trung gian để lưu mối quan hệ nhiều nhiều của Ban và User
class Banship(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ban = models.ForeignKey(Ban,on_delete=models.CASCADE)

# PTteam mà tv đó đang ở
class Powerteam(models.Model):
    user = models.ManyToManyField(User,through="PTteamship")
    name = models.CharField(max_length=100,null=False,blank=False)
    headOfPTteam = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self) -> str:
        return self.name
# Mô hình trung gian để lưu mối quan hệ nhiều nhiều của PTteam và User
class PTteamship(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    PT = models.ForeignKey(Powerteam,on_delete=models.CASCADE)
