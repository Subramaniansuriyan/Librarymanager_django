from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password
from library.models import Category,Book,Lend_details
from django.core.files.base import ContentFile
import base64
import imghdr
import six
import uuid
import json

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True
    )
   
    password = serializers.CharField(
        required=True
    )

    def validate(self, validated_data):
        user = User.objects.filter(username=validated_data["username"])

        if not user.exists():
            raise serializers.ValidationError({"username":"user not found"})
        
        if not check_password(validated_data["password"],user.first().password):
            raise serializers.ValidationError({'password':"Password Incorrect"})

        return validated_data

class UserSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=15,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        required=True,
        write_only=True)

    def create(self,validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'],
            validated_data['password']
        )
        return user


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "id","username","email","is_staff"

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
            	# Break out the header from the base64 content
            	header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
            	decoded_file = base64.b64decode(data)
            except TypeError:
            	self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

    	extension = imghdr.what(file_name, decoded_file)
    	extension = "jpg" if extension == "jpeg" else extension

    	return extension



class LibraryBookSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length = 100,
        required = True,
        validators=[UniqueValidator(queryset=Book.objects.all())])
    description = serializers.CharField(allow_blank = True)
    publisher = serializers.CharField(required = True)
    author = serializers.CharField(required = True)
    categories = serializers.IntegerField(required = True)
    book_image = serializers.ImageField(
        max_length=None, use_url=True,required=True
    )


    def validate(self,validated_data):
        category = Category.objects.filter(id = validated_data['categories'])

        if not category.exists():
            raise serializers.ValidationError({'response':'category_not_found'})

        return validated_data

    def create(self,validated_data):
        category = Category.objects.get(id = validated_data['categories'])

        book = Book.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            publisher = validated_data['publisher'],
            author = validated_data['author'],
            categories = category,
            book_image = validated_data['book_image']
        )
        return validated_data



class BookSerializer(serializers.ModelSerializer):
    book_image_url = serializers.SerializerMethodField('get_photo_url')
    class Meta:
        model = Book
        fields = ["id","title","description","publisher","author","categories","book_image_url","is_available","book_image"]


    def get_photo_url(self, obj):
        request = self.context.get('request')
        
        if obj.book_image:
            photo_url = obj.book_image.url
        else:
            photo_url = None

        return request.build_absolute_uri(photo_url)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
