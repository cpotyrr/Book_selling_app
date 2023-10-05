# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from book_selling.models import Book, Author


class AuthorSerializer(ModelSerializer):
    fullname = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('fullname', 'books')

    def get_fullname(self, obj):
        return obj.get_fullname()

    def get_books(self, obj):
        books = obj.get_books()
        return {'titles': books, 'book_count': len(books)},


class RawAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'middle_name')


class BookSerializer(ModelSerializer):
    authors = RawAuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ('title', 'authors', 'price')
