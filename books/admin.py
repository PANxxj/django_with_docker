from django.contrib import admin
from .models import Author, Category, Book

# Admin configuration for Author model
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  # Fields to display in the list view
    search_fields = ('name',)  # Make the 'name' field searchable
    list_filter = ('created', 'modified')  # Add filters to the sidebar based on created/modified date

admin.site.register(Author, AuthorAdmin)

# Admin configuration for Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  # Fields to display in the list view
    search_fields = ('name',)  # Make the 'name' field searchable
    list_filter = ('created', 'modified')  # Add filters to the sidebar based on created/modified date

admin.site.register(Category, CategoryAdmin)

# Admin configuration for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'mrp', 'category', 'created', 'modified')  # Display key fields
    search_fields = ('name', 'category__name')  # Make the book name and category name searchable
    list_filter = ('category', 'created', 'modified')  # Filter by category and dates
    ordering = ('-created',)  # Order books by created date (newest first)

    # Inline editing for Many-to-Many relation (authors)
    filter_horizontal = ('author',)  # This adds a nice interface for managing Many-to-Many relationships

admin.site.register(Book, BookAdmin)
