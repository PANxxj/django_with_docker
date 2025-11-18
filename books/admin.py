from django.contrib import admin
from .models import Author, Publisher, Category, Tag, Book, Sale, Review

# Admin configuration for Author model
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  # Fields to display in the list view
    search_fields = ('name',)  # Make the 'name' field searchable
    list_filter = ('created', 'modified')  # Add filters to the sidebar based on created/modified date

admin.site.register(Author, AuthorAdmin)

# Admin configuration for Publisher model
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created', 'modified')  # Show name and address
    search_fields = ('name', 'address')  # Allow search by publisher name and address
    list_filter = ('created', 'modified')  # Filter by created/modified dates

admin.site.register(Publisher, PublisherAdmin)

# Admin configuration for Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  # Fields to display in the list view
    search_fields = ('name',)  # Make the 'name' field searchable
    list_filter = ('created', 'modified')  # Add filters to the sidebar based on created/modified date

admin.site.register(Category, CategoryAdmin)

# Admin configuration for Tag model
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')  # Show name in the list view
    search_fields = ('name',)  # Allow searching by tag name
    list_filter = ('created', 'modified')  # Filter by created/modified dates

admin.site.register(Tag, TagAdmin)

# Admin configuration for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'mrp', 'category', 'publisher', 'created', 'modified')  # Display key fields
    search_fields = ('name', 'category__name', 'publisher__name')  # Search by book name, category, and publisher
    list_filter = ('category', 'publisher', 'created', 'modified')  # Filters for category, publisher, and dates
    ordering = ('-created',)  # Order books by created date (newest first)

    # Inline editing for Many-to-Many relation (authors)
    filter_horizontal = ('author',)  # This adds a nice interface for managing Many-to-Many relationships

    # Add inlines for related Sales, Reviews, and Inventory
    inlines = []

admin.site.register(Book, BookAdmin)

# Admin configuration for Sale model
class SaleAdmin(admin.ModelAdmin):
    list_display = ('book', 'sale_date', 'quantity_sold', 'total_price', 'created', 'modified')
    search_fields = ('book__name', 'sale_date')  # Search by book name and sale date
    list_filter = ('sale_date', 'created', 'modified')  # Filter by sale date, created/modified date

admin.site.register(Sale, SaleAdmin)

# Admin configuration for Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer_name', 'rating', 'created', 'modified')  # Display review details
    search_fields = ('book__name', 'reviewer_name')  # Search by book name and reviewer
    list_filter = ('rating', 'created', 'modified')  # Filter by rating and created/modified dates

admin.site.register(Review, ReviewAdmin)

