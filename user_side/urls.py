from django.urls import path
from seamless import settings
from user_side import views
from django.conf.urls.static import static

app_name = 'user_side'

urlpatterns = [

    path('', views.landing_handler, name='landing'),
    path('product-details/<int:id>', views.product_details, name='product_details'),
    path('add-to-wishlist/<int:id>/', views.add_wishlist, name='add_wishlist'),
    path('view-from-wishlist/', views.view_wishlist, name='view_wishlist'),
    path('delete-from-wishlist/<int:id>/', views.delete_wishlist, name='delete_wishlist'),
    path('product-list-here/' , views.product_list, name='product_list'),
    path('product-list-here/<int:id>' , views.product_list, name='product_list'),
    path('product-order-by-here/<str:order_by>' , views.product_sort, name='product_sort'),
    path('view-all-category' , views.category_page, name='category_page'),
    path('all_search' , views.all_search, name='all_search'),
    path('change_profile_image/' , views.change_profile_image, name='change_profile_image'),
    

    



    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)