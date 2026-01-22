from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser
from .manager import MyUserManager
import uuid

# Create your models here.
class MyUser(AbstractBaseUser,PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True)
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(max_length=250,unique=True)
    ph_no = models.PositiveBigIntegerField(unique=True)

    role = models.CharField(choices=[('student','STUDENT'),('instructor','INSTRUCTOR'),('admin','ADMIN')])
    profile_pic = models.ImageField(default='profiles/default_avatar.png',upload_to='profiles/',blank=True,null=True)
    bio = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','ph_no']

    def __str__(self):
        return self.username

    manager = MyUserManager()