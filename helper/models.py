from django.db import models
import uuid

class CreationModificationBaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=False,auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f'{self.__class__.__name__} ({self.id})'