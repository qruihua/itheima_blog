from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 用户信息
class User(AbstractUser):

    # 电话号码字段
    # unique 为唯一性字段
    mobile = models.CharField(max_length=20, unique=True,blank=True)

    # 头像
    # upload_to为保存到响应的子目录中
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    # 个人简介
    user_desc = models.TextField(max_length=500, blank=True)

    # 修改认证的字段
    USERNAME_FIELD = 'mobile'

    #创建超级管理员时需要必须设置的字段
    REQUIRED_FIELDS = ['username','email']