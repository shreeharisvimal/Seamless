from django.urls import path
from brands import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'brands'

urlpatterns = [
    
    path('', views.brands_handler, name='brands_view'),
    path('add-brand/', views.brands_add, name='brands_add'),
    path('status-brand/<int:id>', views.brands_status, name='brands_status'),
    path('delete-brand/<int:id>', views.brands_delete, name='brands_delete'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
