from django.urls import path
from wallet import views

app_name = 'wallet'


urlpatterns = [
    
    path('wallet-view', views.wallet_view, name='wallet_view'),
    path('wallet-recived', views.credit, name='credit'),
    path('wallet-seampay-razor', views.seampay_razor, name='seam_razor'),

    


]
