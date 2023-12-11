from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'order'

urlpatterns = [
    path('order-manage-view', views.order_view, name="order_view"),
    path('order_coupon-view', views.order_coupon, name="order_coupon"),
    path('order_coupon_delete-view', views.order_coupon_delete, name="order_coupon_delete"),
    path('view-place_order', views.place_order, name="place_order"),
    path('view-order_details', views.order_details, name="order_status"),
    path('view-order_listing/<int:id>', views.order_listing, name="order_listing"),
    path('view-cancel_order/<int:id>/', views.cancel_order, name="cancel_order"),
    path('view-cancel_order_request/<int:id>/', views.cancel_order_request, name="cancel_order_request"),
    path('view-admin_order', views.admin_order_view, name="admin_order_view"),
    path('admin_order_item_details/<int:id>/', views.admin_order_item_details, name="admin_order_item_details"),
    path('admin_order_item_view/<int:id>/', views.admin_order_item_view, name="admin_order_item_view"),
    path('admin_order_status/', views.admin_order_status, name="admin_order_status"), 
    path('admin_order_status_all/', views.admin_order_status_all, name="admin_order_status_all"), 
    path('user-order-tracking/', views.user_order_tracking, name="user_order_tracking"), 
    path('view-invoice_showing', views.invoice_showing, name="invoice_showing"),
    path('order_user_view', views.order_user_view, name="order_user_view"),
    path('pay_with_razor', views.pay_with_razor, name="pay_with_razor"),
    path('user_details_views/<int:id>', views.user_details_views, name="user_details_views"),
    path('order_search', views.order_search, name="order_search"),


    




    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)