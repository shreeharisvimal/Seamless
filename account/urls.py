from account import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('add-address/', views.add_address, name='add_address'),
    path('manage-view-address/', views.manage_address, name='manage_address'),


    
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
