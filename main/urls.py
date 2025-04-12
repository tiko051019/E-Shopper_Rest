from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('logout/',LogoutAllDevicesAPIView.as_view()),

    path('forgot_code/',ForgotPasswordAPIView.as_view()),
    path('vercode/<uidb64>/<token>/',VerifyCodeAPIView.as_view()),
    path('reset_password/<uidb64>/<token>/',ResetPasswordAPIView.as_view()),
    
    path('carousel/',CarouselFunction),
    path('maininfo/',MainInfoFunction),
    path('category/',CategoryFunction),
    path('subcategory/',SubcategoryFunction),
    path('itemsname/',ItemsnameFunction),
    path('items/',ItemsFunction),
    path('items_filtered_by_name/<str:item_name>/',ItemsFilteredByNameFunction),
    path('products_image/',ProductsFunction),
    path('item_details/<int:id>/',ItemsDetailsFunction),
    path('items_filtered_by_categ/<str:categ>/<str:subcat>/',ItemsFilterByCategORSubcat),
    path('gallery/',GalleryFunction),
    path('contact_message/',ContactMessageFunction),
    path('review_message/<int:id>/',ReviewMessageFunction),

    path('usersave_items/<uidb64>/<token>/<int:item_id>/',UserSaveFunction),
    path('save_items_id_function/<int:user_id>/',SaveItems_Id_Function),
    path('add_quantity/<int:user_id>/<int:item_id>/',Item_Quantity_Add),
    path('remove_quantity/<int:user_id>/<int:item_id>/',Item_Quantity_Remove),

    path('taxes/',TotalTaxesFunction),
    path('total_price/<int:user_id>/',TotalPriceFunction),
    path('userinfo/<int:user_id>/',UserInfoFunction),
    path('make_payment/<int:user_id>/',PaymentFunction),
    path('payments_history/<int:user_id>/',PaymentHistoryFunction),
    path('page404/',Page404Function),

    ]