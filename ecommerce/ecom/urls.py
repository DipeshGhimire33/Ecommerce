from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #------PRODUCT URLS------
    path("", views.index, name='index'),
    path("product_list", views.product_list,name='product_list'),
    path("add_product/", views.add_product, name='add_product'),
    path("edit_product/<int:id>/", views.edit_product, name='edit_product'),
    path("delete_product/<int:id>/", views.delete_product, name='delete_product'),
    path("product/<int:id>/", views.product_detail, name='product_detail'),
    path("products/<str:category>/", views.category_product_list, name='category_product_list'),

    #-------REGISTRATION AND AUTHENTICATION URLS------
    path("register/", views.register, name='register'),

    #-------SEARCH URLS------
    path("ecom/search/", views.search_product, name='search_product'),

    #-------CATEGORY AND REVIEW URLS------
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('review/add/<int:product_id>/', views.review_add, name='review_add'),

    path("index/", views.index, name='index'),

    #------CART AND ORDER URLS------
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name='add_to_cart'),
    path("cart/", views.cart, name='cart'),
    path("remove_from_cart/<int:product_id>/", views.remove_from_cart, name='remove_from_cart'),
     path("update-cart/<int:product_id>/", views.update_cart_item, name="update_cart_item"),
    path("place-order/", views.place_order, name="place_order"),
    path("confirm-order/", views.confirm_order, name="confirm_order"),

    #-------USER PROFILE URLS------
    path("profile/", views.profile, name="profile"),

    #----Report URLS------
    path("report/", views.report, name="report"),
   
   

]