import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Author, Publisher, Category, Tag, Book, Sale, Review

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with dummy data for all models'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Clear existing data from relevant tables
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        Book.objects.all().delete()
        Sale.objects.all().delete()
        Review.objects.all().delete()

        self.stdout.write("Seeding new data...")

        # -----------------------
        # Create Authors
        # -----------------------
        authors = []
        for _ in range(15):
            author = Author.objects.create(name=fake.name())
            authors.append(author)

        # -----------------------
        # Create Publishers
        # -----------------------
        publishers = []
        for _ in range(8):
            publisher = Publisher.objects.create(
                name=fake.company(),
                address=fake.address()
            )
            publishers.append(publisher)

        # -----------------------
        # Create Categories
        # -----------------------
        categories_list = [
            'Fiction', 'Science', 'History', 'Philosophy', 'Art',
            'Fantasy', 'Biography', 'Technology', 'Sports', 'Travel'
        ]
        categories = []
        for cat_name in categories_list:
            category = Category.objects.create(name=cat_name)
            categories.append(category)

        # -----------------------
        # Create Tags
        # -----------------------
        tag_names = [
            "Classic", "Adventure", "Magic", "Programming", "Romance",
            "Mystery", "AI", "Python", "Thriller", "Science Fiction",
            "Drama", "Space", "Nature", "Horror", "Crime",
            "Culture", "Psychology", "Education", "Kids", "Business"
        ]
        tags = []
        for t in tag_names:
            tag = Tag.objects.create(name=t)
            tags.append(tag)

        # -----------------------
        # Create Books + related data
        # -----------------------
        for _ in range(200):
            book_name = fake.sentence(nb_words=4)
            price = round(random.uniform(10.0, 200.0), 2)
            discount = round(random.uniform(1.0, 20.0), 2)

            # Create the book object
            book = Book.objects.create(
                name=book_name,
                price=price,
                discount=discount,
                mrp=price + round(random.uniform(5.0, 20.0), 2),
                category=random.choice(categories),
                publisher=random.choice(publishers)
            )

            # Assign multiple authors (1 to 3 authors per book)
            book.author.add(*random.sample(authors, random.randint(1, 3)))

            # Assign tags (1 to 4 tags per book)
            book.tags.add(*random.sample(tags, random.randint(1, 4)))

            # -----------------------
            # Create Sales for the book
            # -----------------------
            for _ in range(random.randint(1, 10)):
                qty = random.randint(1, 10)
                Sale.objects.create(
                    book=book,
                    sale_date=fake.date_between(start_date="-1y", end_date="today"),
                    quantity_sold=qty,
                    total_price=qty * book.price
                )

            # -----------------------
            # Create Reviews for the book
            # -----------------------
            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    book=book,
                    reviewer_name=fake.name(),
                    review_text=fake.text(),
                    rating=random.randint(1, 5)
                )

        self.stdout.write(self.style.SUCCESS('Dummy Data Generation Completed Successfully!'))
