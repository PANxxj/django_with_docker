from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser
from helper.models import CreationModificationBaseModel
from .managers import CustomUserManager
from helper.functions import validate_phone_number

class CustomUser(AbstractBaseUser,PermissionsMixin,CreationModificationBaseModel):
    email = models.EmailField(unique=True,null=True,blank=True,db_index=True)
    phone_no = models.PositiveBigIntegerField(unique=True,null=False,blank=False,db_index=True,validators=[validate_phone_number])
    password = models.CharField(max_length=250,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email or 'No Email yet'}-{self.phone_no}"