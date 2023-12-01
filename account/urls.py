from account import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('add-address/', views.add_address, name='add_address'),
    path('manage-view-address/', views.manage_address, name='manage_address'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
    path('del_address/<int:id>', views.del_address, name='del_address'),
    path('Account-details-edit/', views.account_edit, name='account_edit'),








    
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
