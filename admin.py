from django.contrib import admin

# Register your models here.
from book_selling.models import Book, Author, PurchaseRequest

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(PurchaseRequest)
