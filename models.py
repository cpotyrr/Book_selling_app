import datetime

from django.contrib.auth.models import User
from django.db import models

from BookSelling.settings import USER_CREDENTIALS_MAX_LENGTH, TITLE_MAX_LENGHT, MAX_PRICE_FOR_BOOKS, \
    TEL_NUMBER_LENGHT_MAX
from BookSelling.validators import validate_phone_number


class Author(models.Model):
    first_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=False,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=True,
                                 verbose_name='Фамилия')
    middle_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=False,
                                   verbose_name='Отчество')

    def get_fullname(self):
        if self.middle_name:
            return '{} {} {}'.format(self.first_name, self.last_name, self.middle_name)
        else:
            return '{} {}'.format(self.first_name, self.last_name)

    def get_books(self):
        titles = Book.objects.filter(authors=self).values('title')
        return list(titles)


class Book(models.Model):
    title = models.CharField(max_length=TITLE_MAX_LENGHT, blank=False)
    authors = models.ManyToManyField('Author',
                                     related_name="authors",
                                     verbose_name="Авторы")
    price = models.DecimalField(decimal_places=2, max_digits=MAX_PRICE_FOR_BOOKS)


class PurchaseRequest(models.Model):
    book = models.ForeignKey('Book',
                             related_name="book",
                             verbose_name="Книга", on_delete=models.CASCADE,
                             null=True)  # better to realize as many to many
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    tel_number = models.CharField(max_length=TEL_NUMBER_LENGHT_MAX, blank=False, validators=[validate_phone_number])
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    request_date = models.DateField(default=datetime.date.today)
