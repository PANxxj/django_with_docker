import random
from faker import Faker
from books.models import Author, Category, Book  # Replace 'yourapp' with your app's name

fake = Faker()

# Create random Authors
def create_authors(num=50):
    authors = []
    for _ in range(num):
        author_name = fake.name()
        author = Author.objects.create(name=author_name)
        authors.append(author)
    return authors

# Create Categories
def create_categories():
    categories = ['Fiction', 'Science', 'History', 'Philosophy', 'Art', 'Fantasy', 'Biography', 'Technology']
    category_objs = []
    for category_name in categories:
        category = Category.objects.create(name=category_name)
        category_objs.append(category)
    return category_objs

# Create Books
def create_books(authors, categories, num=50):
    for _ in range(num):
        book_name = fake.sentence(nb_words=4)  # Generate a random book name
        price = round(random.uniform(5.0, 100.0), 2)
        discount = round(random.uniform(1.0, 15.0), 2)
        mrp = price + round(random.uniform(2.0, 10.0), 2)
        category = random.choice(categories)
        
        # Create Book
        book = Book.objects.create(
            name=book_name,
            price=price,
            discount=discount,
            mrp=mrp,
            category=category
        )
        
        # Assign random authors (up to 3 authors per book)
        num_authors = random.randint(1, 3)
        book_authors = random.sample(authors, num_authors)
        book.author.add(*book_authors)  # Add multiple authors
    
    print(f"Inserted {num} books with random data!")

# Main function to insert data
def insert_dummy_data():
    authors = create_authors(10)  # Create 50 authors
    categories = create_categories()  # Create categories
    create_books(authors, categories, 100)  # Create 50 books

# Insert the data
insert_dummy_data()
