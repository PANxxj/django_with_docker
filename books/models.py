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
    
class Publisher(CreationModificationBaseModel):
    name = models.CharField(max_length=255, db_index=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(CreationModificationBaseModel):
    name = models.CharField(max_length=255,db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        
class Tag(CreationModificationBaseModel):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Book(CreationModificationBaseModel):
    author = models.ManyToManyField(Author, blank=True)  # Many-to-Many relationship with Author
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Many-to-One relationship with Category
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)  # Many-to-One relationship with Publisher
    name = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(Tag, blank=True)  # Many-to-Many relationship with Tag

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['publisher']),
        ]

    
    
class Sale(CreationModificationBaseModel):
    book = models.ForeignKey(Book, related_name='sales', on_delete=models.CASCADE)
    sale_date = models.DateField()
    quantity_sold = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.book.name} on {self.sale_date}"

class Review(CreationModificationBaseModel):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review of {self.book.name} by {self.reviewer_name}"
