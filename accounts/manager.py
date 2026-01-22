from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self,email,username,ph_no='',password=None,**extra_fields):
        if not email:
            raise ValueError('email is necessary')
        user = self.model(
            email = self.normalize_email(email),**extra_fields
        )
        user.username = username
        user.ph_no = ph_no
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_instructor(self,email,username,ph_no='',password=None,**extra_fields):
        extra_fields.setdefault('is_instructor',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_approved',False)
        user = self.create_user(email=email,username=username,ph_no=ph_no,password=password,**extra_fields)
        return user
    
    def create_student(self,email,username,ph_no='',password=None,**extra_fields):
        extra_fields.setdefault('is_student',True)
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_approved',True)
        user = self.create_user(email=email,username=username,ph_no=ph_no,password=password,**extra_fields)
        return user
    
    def create_superuser(self,email,username,ph_no='',password=None,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role",'admin')
        user = self.create_user(email=email,username=username,ph_no=ph_no,password=password,**extra_fields)
        return user