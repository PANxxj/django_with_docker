from helper.models import CreationModificationBaseModel
from django.db import models

class Author(CreationModificationBaseModel):
    name = models.CharField(max_length=255,db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
    
class Category(CreationModificationBaseModel):
    name = models.CharField(max_length=255,db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        
class Book(CreationModificationBaseModel):
    author = models.ManyToManyField(to=Author,blank=True)
    category = models.ForeignKey(to=Category,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed this line
    discount = models.DecimalField(max_digits=10, decimal_places=2)  # Added decimal_places
    mrp = models.DecimalField(max_digits=10, decimal_places=2) 
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    
