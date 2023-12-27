"""
URL configuration for seamless project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from social_django.views import auth, complete
from django.conf.urls.static import static
from seamless import settings



urlpatterns = [
    path('admin-orginal/', admin.site.urls), # for  Default django admin page

   path('', include('authenticator.urls')),    # for login sign up  management

   path('', include('user_side.urls')), # for client side works management

   path('my_admin/', include('admin_side.urls')), # for admin side works management

   path('cata/', include('category_manage.urls')),  # for catagory management

   path('pro/', include('products.urls')),  # for product management

   path('brand/', include('brands.urls')), # for brands management

    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/', auth, name='social-auth'),
    path('auth/complete/google-oauth2/', complete, name='google-oauth2-complete'),

    path('cart-management/', include('cart.urls')), # for cart management

    path('account-management/', include('account.urls')), # for cart management

    path('order-management/', include('order_management.urls')), # for ordering and other stuffs


    path('wallet-management/', include('wallet.urls')), # for wallet management and other stuffsreview

    path('review_management_review_management/', include('review_management.urls')), # for wallet management and other stuffsreview



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)