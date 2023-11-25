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
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)