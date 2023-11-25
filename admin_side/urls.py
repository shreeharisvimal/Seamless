from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from admin_side import views



app_name = 'admin_side'

urlpatterns = [
    path('logout/', views.logout_handler, name='logout'),
    path('', views.admin_login_handler, name='admin_login_handler'),
    path('admin_dashboard/', views.admin_dash_handler, name='admin_dash_handler'),
    path('admin_customer/', views.admin_user_handler, name='admin_user_manage'),
    path('customer_status/<int:user_id>', views.customer_status, name='customer_status'),
    path('customer-search/', views.customer_search, name='customer_search'),
    path('attribute-search/', views.attribute_search, name='attribute_search'),
    path('variant-search/', views.variant_search, name='variant_search'),
    path('product-search/', views.product_search, name='product_search'),
    path('category-search/', views.category_search, name='category_search'),
    path('brand-search/', views.brand_search, name='brand_search'),
    path('coupon-search/', views.coupon_search, name='coupon_search'),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)