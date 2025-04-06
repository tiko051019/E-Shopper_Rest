from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework import status 


class AuthorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def USerEmailSearching(self,email):
        if not User.objects.filter(email = email).exists():
            return Response({'message': 'Email is not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Email is  found'}, status=status.HTTP_202_ACCEPTED)


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'

class MainInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MainInfo
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ItemsnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsName
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        
class ItemsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsDetails
        fields = '__all__'

class ItemsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsImages
        fields = '__all__'
        
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class ReviewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMessage
        fields = '__all__'

class UserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSave
        fields = '__all__'

class TotalTaxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total_Taxes
        fields = '__all__'

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments_History
        fields = '__all__'
    
class model404Serializer(serializers.ModelSerializer):
    class Meta:
        model = model404
        fields = '__all__'