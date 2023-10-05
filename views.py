from django.http import JsonResponse

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from BookSelling.validators import validate_phone_number
from book_selling.models import Author, Book, PurchaseRequest
from book_selling.serializers import BookSerializer, AuthorSerializer
from book_selling.utils import send_superuser_emails


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_authors(request):
    """
    :return: fio, books, books_count
    Example:

    [{"fullname": "FIRST_NAME MIDDLE_NAME LAST_NAME",
    "books": [{"title": "TITLE"}, {"title": "TITLE"}, books_count: 2]}]}]
    """
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)

    return JsonResponse(data=serializer.data, json_dumps_params={'ensure_ascii': False}, status=200, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_books(request):
    """
    :return: title, authors, price
    Example:

    [{"title": "TITLE", "authors": [{"first_name": "FIRST_NAME", "last_name": "LAST_NAME", "middle_name": "MIDDLE_NAME"}],
    "price": "100.00"}]

    """
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return JsonResponse(data=serializer.data, json_dumps_params={'ensure_ascii': False}, status=200, safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_purchase_request(request):
    """
    Create Purchase Request

    keys:
    book_id
    tel_number
    comment
    """
    # Get params from data
    book_id = request.data.get('book_id')
    if not book_id:
        return JsonResponse(data='{}: This field is required'.format(book_id))

    comment = request.data.get('comment')

    tel_number = request.data.get('tel_number')
    if not tel_number:
        return JsonResponse(data='{}: This field is required'.format(tel_number), status=404, safe=False)

    validate_phone_number(tel_number)

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse(data='Book with id={} does not exists'.format(book_id), status=404, safe=False)

    purchase_request = PurchaseRequest(book=book, user=request.user, tel_number=tel_number, comment=comment)
    purchase_request.save()

    send_superuser_emails.delay('Title example', 'email body')

    return JsonResponse(data='ok', status=200, safe=False)
