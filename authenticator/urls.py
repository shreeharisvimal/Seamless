from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



app_name = 'authentication'

urlpatterns = [
    path('otp-verify/',views.otp_verify, name='otp_verify'),
    path('login/', views.login_handler, name='login_handler'),
    path('logout/', views.logout_handler, name='logout'),
    path('sign/', views.sign_handler, name='sign_handler'),


    



   
    ] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)