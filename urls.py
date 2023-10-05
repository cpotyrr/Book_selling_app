from django.urls import path

from book_selling import views

urlpatterns = [
    path('authors/', views.get_authors),
    path('books/', views.get_books),
    path('purchase_request/', views.create_purchase_request)
]
