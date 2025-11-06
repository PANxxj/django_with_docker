from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model."""
    
    def create_user(self,phone_no,email=None,password=None,**extra_fields):
        if not phone_no:
            raise ValueError('phone number is required')
        email = self.normalize_email(email)
        user = self.model(phone_no=phone_no,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,phone_no,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff for superuser must be true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser for superuser must be true')
        
        return self.create_user(phone_no,email,password,**extra_fields)
    