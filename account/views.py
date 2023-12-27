import traceback
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from account.forms import ImageForm
from wallet.models import SeamPay
from django.contrib import messages
from psycopg import IntegrityError
from account.models import Address
from django.db.models import Q
from user_side.models import NewUser
from .models import UserProfile

@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def my_dashboard(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')

    shipping = Address.objects.filter(user = request.user, is_shipping=True, is_default=True)
    billing = Address.objects.filter(user = request.user, is_billing=True, is_default=True)
    myuser = None
    try:
        myuser = UserProfile.objects.get(user = request.user)
    except Exception as e:
        print(f'the error {e}')
    context = {
        'shipping': shipping ,
        'billing':  billing ,
        'myuser':  myuser ,
        'seam': SeamPay.objects.get(user = request.user),
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
    
    try:
        context = {
        'shipping_address':Address.objects.filter(Q(is_shipping = True) & Q(user= request.user) & ~Q(is_default = True)),
        'billing_address':Address.objects.filter(Q(is_billing = True) & Q(user= request.user) & ~Q(is_default = True)),
        'default_billing':Address.objects.filter(Q(is_billing = True) & Q(user= request.user) & Q(is_default = True)),
        'default_shipping':Address.objects.filter(Q(is_shipping = True) & Q(user= request.user) & Q(is_default = True)),
        'all_address':  Address.objects.filter(user = request.user, is_billing=False, is_shipping=False),
        }
    except Exception as e:
        print(f'the error is {e}')
    
    return render(request, 'user/dashboard/manage_address.html',context)


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def edit_address(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    address = get_object_or_404(Address, (Q(user = request.user) & Q(id=id)))
    if request.method == "POST":
        user = request.user
        print("Attempting to create Address with the following data:")
        print(f"User: {user}")
        print(f"Name: {request.POST.get('name')}")
        print(f"country: {request.POST.get('country')}")
        print(f"house_address: {request.POST.get('house_address')}")
    try:
        address.name =request.POST['name']
        address.phone_number = request.POST['phone_number']
        address.address_one = request.POST['house_address']
        address.city =request.POST['city']
        address.state =request.POST['state']
        address.country = request.POST['country']
        address.pincode =request.POST['pincode']
        address.is_billing = True if 'as_billing' in request.POST else False
        address.is_shipping = True if 'as_shipping' in request.POST else False
        address.is_default = True if 'set_default' in request.POST else False
        address.save()
        messages.success(request,f'the address {address.address_one} has saved changes')
        return redirect('account:manage_address')
    except:
        pass
    context = {
        'add':address,
    }
    return render(request, 'user/dashboard/address_edit.html', context)

def del_address(request,id):
    address = get_object_or_404(Address, user = request.user, id=id)
    messages.info(request,f'the address {address} has been deleted')
    address.delete()
    return redirect('account:manage_address')


def account_edit(request):
    if request.method =="POST":
        acc_user, check = UserProfile.objects.get_or_create(user = request.user)
        acc_user.full_name = request.POST['name']
        acc_user.phone_number = request.POST['phnumber'] if request.POST['phnumber'] else request.user.phone_number
        acc_user.email = request.POST['email'] if request.POST['email'] else request.user.email
        # if request.FILES.get('Profile_img'):
        #     acc_user.profile_pic = request.FILES.get('Profile_img')
        acc_user.nationality = request.POST['nationality']
        if not acc_user.DOB:
            acc_user.DOB = request.POST['DOB']
        try:
            acc_user.save()
            messages.success(request,'Account details updated successfully!')
            return redirect('account:account_edit')
        except Exception as e:
            print(F'the error {e}')
            messages.error(request,f"An error occured while updating your profile.{e}")
            pass
    myuser = UserProfile.objects.get_or_create(user = request.user)
    myuser = get_object_or_404(UserProfile, user = request.user)
    print(myuser)
    context = {
        'myuser' : myuser
    }

    return render(request, 'user/dashboard/edit_account.html', context)

def pic_uploading(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'works'})
    context = {'form': form}
    return render(request, 'user/dashboard/edit_account.html', context)

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:account_edit')


