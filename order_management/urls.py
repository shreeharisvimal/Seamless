from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'order'

urlpatterns = [
    path('order-manage-view', views.order_view, name="order_view"),
    path('order_coupon-view', views.order_coupon, name="order_coupon"),
    path('order_coupon_delete-view', views.order_coupon_delete, name="order_coupon_delete"),

    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)