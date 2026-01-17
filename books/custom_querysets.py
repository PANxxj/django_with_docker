from django.db import models
from django.db.models import Avg, Sum, Count
from django.utils.timezone import now


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_deleted=False)

    def inactive(self):
        return self.filter(is_active=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class BookQuerySet(BaseQuerySet):
    def by_category(self, category_id):
        return self.filter(category_id=category_id)

    def by_publisher(self, publisher_id):
        return self.filter(publisher_id=publisher_id)

    def priced_between(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_avg_rating(self):
        return self.annotate(avg_rating=Avg('reviews__rating'))

    def best_sellers(self):
        return self.annotate(
            total_sold=Sum('sales__quantity_sold')
        ).order_by('-total_sold')


class AuthorQuerySet(BaseQuerySet):
    def search(self, name):
        return self.filter(name__icontains=name)

    def with_books(self):
        return self.filter(book__isnull=False).distinct()


class SaleQuerySet(BaseQuerySet):
    def today(self):
        return self.filter(sale_date=now().date())

    def between_dates(self, start_date, end_date):
        return self.filter(sale_date__range=(start_date, end_date))

    def total_revenue(self):
        return self.aggregate(total=Sum('total_price'))['total']


class ReviewQuerySet(BaseQuerySet):
    def high_rated(self):
        return self.filter(rating__gte=4)

    def for_book(self, book_id):
        return self.filter(book_id=book_id)


class CategoryQuerySet(BaseQuerySet):
    def popular(self):
        return self.annotate(
            book_count=Count('book')
        ).order_by('-book_count')


class TagQuerySet(BaseQuerySet):
    def search(self, name):
        return self.filter(name__icontains=name)
