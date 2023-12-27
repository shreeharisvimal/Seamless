from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'category_manage'

urlpatterns = [
    path('',views.category_main, name='category_handler'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<slug:slug>/', views.delete_category, name='delete_category'),
    path('status_category/<int:id>/', views.status_category, name='status_category'),
    path('view_categoryoffer/', views.view_categoryoffer, name='view_categoryoffer'),
    path('status_categoryoffer/<int:id>', views.status_categoryoffer, name='status_categoryoffer'),
    path('add_categoryoffer/', views.add_categoryoffer, name='add_categoryoffer'),
    path('delete_categoryoffer/<int:id>/', views.delete_categoryoffer, name='delete_categoryoffer'),
    path('edit_categoryoffer/<int:id>/', views.edit_categoryoffer, name='edit_categoryoffer'),





]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)