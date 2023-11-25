import traceback
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from psycopg import IntegrityError
from account.models import Address
from django.db.models import Q

@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def my_dashboard(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')

    shipping = Address.objects.filter(user = request.user, is_shipping=True)
    billing = Address.objects.filter(user = request.user, is_billing=True)
    context = {
        'shipping': shipping ,
        'billing':  billing ,
    }
    return render(request, 'user/dashboard/dashboard.html',context)

@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def add_address(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    
    if request.method=="POST":
        try:
            user = request.user
            print("Attempting to create Address with the following data:")
            print(f"User: {user}")
            print(f"Name: {request.POST.get('name')}")
            print(f"country: {request.POST.get('country')}")
            print(f"house_address: {request.POST.get('house_address')}")

            Address.objects.create(
                user = user,
                name =request.POST.get('name'),
                phone_number = request.POST.get('phone_number'),
                address_one = request.POST.get('house_address'),
                city =request.POST.get('city'),
                state =request.POST.get('state'),
                country = request.POST.get('country'),
                pincode =request.POST.get('pincode'),
                is_shipping = True if 'as_shipping' in request.POST else False,
                is_billing = True if 'as_billing' in request.POST else False,
            )
            messages.success(request,'the address has been added')
            return redirect('account:add_address')
        except IntegrityError as e:
            messages.warning(request, f'The address could not be added. Error: {str(e)}')
            traceback.print_exc()


    return render(request, 'user/dashboard/address.html')


def manage_address(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    

    context = {
    'shipping_address':Address.objects.filter(Q(is_shipping = True)),
    'billing_address':Address.objects.filter(Q(is_billing = True)),
    }
    return render(request, 'user/dashboard/manage_address.html',context)