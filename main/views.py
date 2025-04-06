from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status 
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import random
from .utils import send_email
from rest_framework.decorators import api_view

#-----------------------------------------Login,Logout,Register----------------------------------------

class RegisterAPIView(APIView):
    def post(self,request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not (username and email and password):
            return Response(data={'error':'All fields are required'})
        if User.objects.filter(username = username).exists():
            return Response(data={'error':'This username already exists'})
        user = User.objects.create_user(username = username,email = email,password = password)
        token,_ = Token.objects.get_or_create(user = user)
        return Response(data={'Token':token.key},status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username,password = password)
        if user:
            token,_=Token.objects.get_or_create(user = user)
            return Response(data={'Token':token.key},status=status.HTTP_302_FOUND)
        else:
            return Response(data={'Error':'Is not found'},status=status.HTTP_304_NOT_MODIFIED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = getattr(request.user, 'auth_token', None)
        if token:
            token.delete()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------Forgot Password--------------------------------------------

class ForgotPasswordAPIView(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            key = User.objects.get(email = email)

            code = random.randint(1000,9999)
            CustomUSer.objects.create(key = key,ver_code = code)
            
            send_email('Message from E-Shopper administration',f'Your verification code is{code}',[email])

            return Response(data = {'message':'Verification code sent to your email'},status=status.HTTP_201_CREATED)
        return Response(data = {'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeAPIView(APIView):
    def post(self,request,id):
        userr = get_object_or_404(CustomUSer,pk = id)
        code_db = userr.ver_code
        code_user = request.data.get('code_user')
        if int(code_db) == int(code_user):
            userr.delete()
            return Response(data={'message':'This code is valid'},status=status.HTTP_200_OK)
        return Response(data={'message':'This code is invalid'},status=status.HTTP_404_NOT_FOUND)

class ResetPasswordAPIView(APIView):
    def post(self,request,id):
        userr = get_object_or_404(User,pk = id) 
        new_password = request.data.get('password1')
        new_password_2 = request.data.get('password2')
        if new_password == new_password_2:
            userr.set_password(new_password)
            userr.save()
            return Response(data = {'message':'Password was updated'},status=status.HTTP_200_OK)
        return Response(data = {'message':'Passwords are not the same'},status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def CarouselFunction(request):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer(queryset,many = True)
    response_data = {
        'carousel':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def MainInfoFunction(request):
    queryset = MainInfo.objects.all()
    serializer_class = MainInfoSerializers(queryset,many = True)
    response_data = {
        'maininfo':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def CategoryFunction(request):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer(queryset,many = True)
    response_data = {
        'category':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def SubcategoryFunction(request):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer(queryset,many = True)
    response_data = {
        'subcategory':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ItemsnameFunction(request):
    queryset = ItemsName.objects.all()
    serializer_class = ItemsnameSerializer(queryset,many = True)
    response_data = {
        'itemsname':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ItemsFunction(request):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer(queryset,many = True)
    response_data = {
        'items':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ItemsFilteredByNameFunction(request,item_name):
    items_name = ItemsName.objects.filter(name = item_name).first()
    queryset = Items.objects.filter(key3 = items_name)
    serializer_class = ItemsSerializer(queryset,many = True)
    response_data = {
        'items_filtered_by_name':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ItemsFilterByCategORSubcat(request,categ,subcat = ' /'):
    category = Category.objects.filter(name = categ).first()
    if subcat != ' /':
        subcategory = SubCategory.objects.filter(subname = subcat).first()
        queryset = Items.objects.filter(key1 = category,key2 = subcategory)
    else:
        queryset = Items.objects.filter(key1 = category)
        print(queryset)
    serializer_class = ItemsSerializer(queryset,many = True)
    response_data = {
        'items_filtered_by_categ_or_subcat':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ProductsFunction(request):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer(queryset,many = True)
    response_data = {
        'products_image':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def ItemsDetailsFunction(request,id):
    queryset_item = Items.objects.filter(pk = id).first()
    queryset_details = ItemsDetails.objects.filter(key = queryset_item)
    serializer_class_items = ItemsSerializer(queryset_item)
    serializer_class_details = ItemsDetailsSerializer(queryset_details,many = True)
    queryset_images = ItemsImages.objects.filter(key = queryset_item)
    serializer_class_images = ItemsImagesSerializer(queryset_images,many = True)
    response_data = {
        'items':serializer_class_items.data,
        'details':serializer_class_details.data,
        'item_images':serializer_class_images.data,
    }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
def GalleryFunction(request):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer(queryset,many = True)
    response_data = {
        'footer_gallery':serializer_class.data
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def ContactMessageFunction(request):
    if request.method == 'POST':
        serializer = ContactMessageSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            message = ContactMessage(
                name = name,
                email = email,
                subject = subject,
                message = message
            )
            message.save()

            send_email('Message from E-Shopper administration','Thank you for your comment',[email])

            return Response({'message':'Message have sent succesfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST','GET'])
def ReviewMessageFunction(request,id):
    queryset_item = Items.objects.filter(pk = id).first()
    queryset_review = ReviewMessage.objects.filter(key = queryset_item)
    serializer_class = ReviewMessageSerializer(queryset_review,many = True)

    response_data = {
        'reviews':serializer_class.data
    }

    if request.method == 'POST':
        serializer = ReviewMessageSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            rating = serializer.validated_data['rating']
            message = serializer.validated_data['message']

            message = ReviewMessage(
                key = queryset_item,
                name = name,
                email = email,
                message = message,
                rating = rating,
            )
            message.save()

            send_email('Message from E-Shopper administration','Thank you for your review',[email])

            return Response({'message':'Review have sent succesfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def UserSaveFunction(request,user_id,item_id):
    userr = get_object_or_404(User, pk=user_id)
    itemm = get_object_or_404(Items, pk=item_id)
    found = UserSave.objects.filter(user_key = userr, item_key = itemm)
    if found:
        UserSave.objects.get(user_key = userr, item_key = itemm).delete()
    else:
        UserSave.objects.create(user_key = userr, item_key = itemm)

    return Response({'message':'Saved'},status=status.HTTP_200_OK)
 
@api_view(['GET'])  
def SaveItems_Id_Function(request,user_id):
    userr = get_object_or_404(User,pk = user_id)
    item_saver = []
    queryset = UserSave.objects.filter(user_key = userr)
    for i in queryset:
        item_saver.append(i.item_key.id)
    serializer_class = UserSaveSerializer(queryset,many = True)
    response_data={
        'item_saver':serializer_class.data
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def Item_Quantity_Add(request,user_id,item_id):
    userr = get_object_or_404(User, pk = user_id)
    itemm = get_object_or_404(UserSave,user_key = userr,item_key = item_id)
    if itemm.quantity >= 10:
        return Response({'message':'Quantity can not be more than 10'},status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        itemm.quantity += 1
        itemm.save()
    return Response({'message':f'Quantity is {itemm.quantity}'},status=status.HTTP_200_OK)

@api_view(['POST'])
def Item_Quantity_Remove(request,user_id,item_id):
    userr = get_object_or_404(User, pk = user_id)
    itemm = get_object_or_404(UserSave,user_key = userr,item_key = item_id)
    if itemm.quantity >= 10:
        return Response({'message':'Quantity can not be less than 1'},status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        itemm.quantity -= 1
        itemm.save()
    return Response({'message':f'Quantity is {itemm.quantity}'},status=status.HTTP_200_OK)

@api_view(['GET'])
def TotalTaxesFunction(request):
    queryset = Total_Taxes.objects.get()
    serializer_class = TotalTaxesSerializer(queryset).data
    return Response(data = {'taxes':serializer_class},status=status.HTTP_200_OK)


@api_view(['POST','GET'])
def UserInfoFunction(request,user_id):
    userr = get_object_or_404(User, pk=user_id)
    queryset = UserInfo.objects.filter(key = userr)
    serializer_class = UserInfoSerializer(queryset,many = True)

    response_data = {
        'user_info':serializer_class.data
    }

    if request.method == 'POST':
        serializer = UserInfoSerializer(data = request.data)

        if serializer.is_valid():
            new_name = serializer.validated_data['name']
            new_surname = serializer.validated_data['surname']
            new_phone = serializer.validated_data['phone']
            new_adress = serializer.validated_data['adress']

        
            info = userr.userinfo_rn.first()
            if new_name:
                info.name = new_name  
            if new_surname:
                info.surname = new_surname 
            if new_phone:
                info.phone = new_phone
            if new_adress:
                info.adress = new_adress
            info.save()

            return Response({'message':'User info has been changed'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def TotalPriceFunction(request,user_id):
    userr = get_object_or_404(User, pk = user_id)
    taxes = Total_Taxes.objects.get()
    saved_in_cart = UserSave.objects.filter(user_key = userr)
    for i in saved_in_cart:
        i.item_key.price_now = (i.item_key.price * (100 - i.item_key.discount))/100
    total = 0
    dct = {}
    for i in saved_in_cart:
        dct[i] = i.item_key.price_now * i.quantity
    total_price = 0
    for i in saved_in_cart:
        total_price += i.item_key.price_now * i.quantity
    total = total_price
    total += taxes.Eco_Tax + taxes.Shipping_Cost
    
    return Response({'Total_Price':total},status=status.HTTP_200_OK)

@api_view(['POST'])
def PaymentFunction(request,user_id):
    userr = get_object_or_404(User, pk = user_id)
    taxes = Total_Taxes.objects.get()
    saved_in_cart = UserSave.objects.filter(user_key = userr)
    for i in saved_in_cart:
        i.item_key.price_now = (i.item_key.price * (100 - i.item_key.discount))/100
    total_price = 0
    for i in saved_in_cart:
        total_price += i.item_key.price_now * i.quantity
    total_price += taxes.Eco_Tax + taxes.Shipping_Cost
    Payments_History.objects.create(key = userr,payment = total_price)
    UserSave.objects.filter(user_key = userr).delete()
    
    return Response({'message':'Payment made succesfully'},status=status.HTTP_200_OK)

@api_view(['GET'])
def PaymentHistoryFunction(request,user_id):
    userr = get_object_or_404(User, pk = user_id)
    queryset = Payments_History.objects.filter(key = userr)
    serializer_class = PaymentHistorySerializer(queryset,many = True)
    return Response({'payments':serializer_class.data},status=status.HTTP_200_OK)

@api_view(['GET'])
def Page404Function(request):
    queryset = model404.objects.all()
    serializer_class = model404Serializer(queryset,many = True)
    return Response({'404_image':serializer_class.data},status=status.HTTP_200_OK)

#------------------------------------------------------------------------------------------------------
