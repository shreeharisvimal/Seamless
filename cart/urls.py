from cart import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name='cart'

urlpatterns = [
    path('coupon-add',views.add_coupon,name='add_coupon'),
    path('coupon-delete/<int:id>/',views.delete_coupon,name='delete_coupon'),
    path('coupon-status/<int:id>/',views.status_coupon,name='status_coupon'),
    path('coupon-view',views.view_coupon,name='view_coupon'),
    path('cart-view',views.view_cart,name='view_cart'),
    path('cart-add/<int:id>/',views.add_cart,name='add_cart'),
    path('cart-delete/<int:id>/',views.delete_cart,name='delete_cart'),
    path('plus-item/<int:id>/',views.item_plus,name='plus_item'),
    path('minus-item/<int:id>/',views.item_minus,name='minus_item'),
    path('remove-coupon/<int:id>/',views.remove_coupon,name='remove_coupon'),
    path('clear_cart/',views.clear_cart,name='clear_cart'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)