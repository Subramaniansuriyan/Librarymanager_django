from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import AllowAny
from library.service import generate_token
from django.contrib.auth import authenticate
from library.models import Book,Category
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .serializers import(
    LoginSerializer,
    UserSerializer,
    MemberSerializer,
    LibraryBookSerializer,
    BookSerializer,
    CategorySerializer,
)
from library.permission import IsAllowedToWrite
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination




@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(username=serializer.data["username"])
        user_auth = authenticate(username=user, password=serializer.data["password"])
        if user_auth:
            authenticated = generate_token(user=user)
        return Response(authenticated, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def add_member(request):
    serilaizer = UserSerializer(data=request.data)
    if serilaizer.is_valid():
        member = serilaizer.save()
        if member:
            return Response(serilaizer.data,status=status.HTTP_201_CREATED)
    return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def list_member(request):
    all_members = User.objects.all()
    serilaizer = MemberSerializer(all_members,many=True)
    if serilaizer:
        return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response({"response":"no_members"},status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def edit_member(request):
    if "id" not in request.data:
        return Response({"response":"id_required"},status=status.HTTP_400_BAD_REQUEST)

    member_id = User.objects.filter(id=request.data.get("id"))

    if not member_id.exists():
        return Response({"response":"member_not_found"},status=status.HTTP_400_BAD_REQUEST)

    member_id = member_id.first()

    serilaizer = MemberSerializer(member_id,data=request.data,partial=True)
    if serilaizer.is_valid():
        member = serilaizer.save()
        if member:
            return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def delete_member(request,id):
    member = User.objects.filter(id=id)

    if not member.exists():
        return Response({"response":"member_not_found"},status=status.HTTP_400_BAD_REQUEST)

    if member.exists():
        member.delete()
        return Response({"response":"deleted_successfully"},status=status.HTTP_200_OK)
    return Response({"response":"not_found"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_book(request):
    serializer = LibraryBookSerializer(data = request.data)
    if serializer.is_valid():
        book = serializer.save()
        if book:
            return Response(serializer.data,status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_book(request):
    all_Books = Book.objects.all()
    serilaizer = BookSerializer(all_Books,many=True,context = {"request":request})
    if serilaizer:
        return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response({"response":"no_books"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    all_category = Category.objects.all()
    serilaizer = CategorySerializer(all_category,many=True)
    if serilaizer:
        return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response({"response":"no_books"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    search = request.query_params.get('search', None)

    if search is None:
        return Response({"response":"id_required_or_book_name_required"},status=status.HTTP_400_BAD_REQUEST)

    data = Book.objects.filter(Q(author__icontains = search) | Q(publisher__icontains = search) |Q(categories__id__icontains = search) | Q(title = search))
    context = BookSerializer(data,many=True,context = {"request":request})
    return Response(context.data,status = status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def edit_book(request,id):
    book_id = Book.objects.filter(id = id)

    if not book_id.exists():
        return Response({"response":"book_not_found"},status=status.HTTP_400_BAD_REQUEST)
    
    book = book_id.first()
    
    serilaizer = BookSerializer(book,data=request.data,partial=True,context = {"request":request})
    if serilaizer.is_valid():
        member = serilaizer.save()
        if member:
            return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def get_book(request,id):   
    book_id = Book.objects.filter(id = id)

    if not book_id.exists():
        return Response({"response":"book_not_found"},status=status.HTTP_400_BAD_REQUEST)
    
    book = book_id.first()
    
    serilaizer = BookSerializer(book,data=request.data,partial=True,context = {"request":request})
    if serilaizer.is_valid():
        member = serilaizer.save()
        if member:
            return Response(serilaizer.data,status=status.HTTP_200_OK)
    return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAllowedToWrite,IsAuthenticated])
def delete_book(request,id):
    book = Book.objects.filter(id=id)

    if not book.exists():
        return Response({"response":"book_not_found"},status=status.HTTP_400_BAD_REQUEST)

    if book.exists():
        book.delete()
        return Response({"response":"deleted_successfully"},status=status.HTTP_200_OK)
    return Response({"response":"not_found"},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def lend_book(request):
    book = request.data.get("book_id")

    if not "book_id" in request.data:
        return Response({"response":"enter_book_id"},status = status.HTTP_400_BAD_REQUEST)

    book = Book.objects.filter(id=book)

    if not book.exists():
        return Response({"response":"book_not_found"},status=status.HTTP_400_BAD_REQUEST)

    if book.first().is_available:
        book.update(is_available=False)
        return Response({"response":"success"},status = status.HTTP_200_OK)
    return Response({"response":"failed"},status = status.HTTP_400_BAD_REQUEST)
