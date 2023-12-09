
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'products'


urlpatterns = [
    
    # path('',views.product_handler,name='product_handler'),
    path('add_product/',views.product_adding,name='product_add'),
    path('product_variant/',views.product_variant,name='product_variant'),
    path('add_attribute/',views.attribute,name='add_attribute'),
    path('attribute_value/',views.attribute_value,name='add_attribute_value'),
    path('view-all/',views.view_attribute,name='view_att'),
    path('attribute-status/<int:id>/', views.attribute_status, name='attribute_status'),
    path('attribute-delete/<int:id>/', views.attribute_delete, name='attribute_delete'),
    path('view-variant/',views.view_variant,name='view_variant'),
    path('variant-status/<int:id>/', views.variant_status, name='variant_status'),
    path('variant-delete/<int:id>/', views.variant_delete, name='variant_delete'),
    path('variant-edit/<int:id>/', views.variant_edit, name='variant_edit'),
    path('view-product/',views.view_product,name='view_product'),
    path('product-status/<int:id>/', views.product_status, name='product_status'),
    path('product-delete/<int:id>/', views.product_delete, name='product_delete'),
    path('product-edit/<int:id>/', views.product_edit, name='product_edit'),
    path('variant-image-edit/<int:id>/<int:var_id>/', views.variant_image_edit, name='variant_image_edit'),
    path('product_select_variant/<int:id>/', views.product_select_variant, name='product_select_variant'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)


