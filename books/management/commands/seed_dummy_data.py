import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Author, Category, Book

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with dummy data for authors, categories, and books'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create Authors
        authors = []
        for _ in range(10):
            author_name = fake.name()
            author = Author.objects.create(name=author_name)
            authors.append(author)

        # Create Categories
        categories_list = ['Fiction', 'Science', 'History', 'Philosophy', 'Art', 'Fantasy', 'Biography', 'Technology']
        categories = []
        for cat_name in categories_list:
            category = Category.objects.create(name=cat_name)
            categories.append(category)

        # Create Books
        for _ in range(100):
            book_name = fake.sentence(nb_words=4)
            price = round(random.uniform(5.0, 100.0), 2)
            discount = round(random.uniform(1.0, 15.0), 2)
            mrp = price + round(random.uniform(2.0, 10.0), 2)
            category = random.choice(categories)

            book = Book.objects.create(
                name=book_name,
                price=price,
                discount=discount,
                mrp=mrp,
                category=category
            )

            num_authors = random.randint(1, 3)
            book_authors = random.sample(authors, num_authors)
            book.author.add(*book_authors)

        self.stdout.write(self.style.SUCCESS('Inserted 100 books with random data!'))
