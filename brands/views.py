from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.cache import cache_control
from django.contrib import messages
from products.models import Brand
from .forms import BrandForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url='authentication:login_handler')
def brands_handler(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')

    brand =Brand.objects.all()
    context={
        'brands': brand,

    }

    return render(request, 'admin/dashboard/brands/brand.html', context)


@cache_control(no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url='authentication:login_handler')
def brands_add(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    if request.method=="POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'the brand add susccesfully')
            return redirect('brands:brands_view')
    else:
        form = BrandForm()

    return render(request, 'admin/dashboard/brands/add_brand.html', {'form': form})


@cache_control(no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url='authentication:login_handler')
def brands_status(request,id):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    if not request.user.is_authenticated:
        return redirect('guest_side:guest_landing')
    if request.method=="POST":
        brand = Brand.objects.get(id = id)
        if brand.is_active == True:
            brand.is_active = False
            brand.save()
            messages.info(request,'The status has been changed to inactive successfully')
        else:
            brand.is_active = True
            brand.save()
            messages.info(request,'The status has been changed active successfully')
        return redirect('brands:brands_view')



@cache_control(no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url='authentication:login_handler')
def brands_delete(request,id):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    if not request.user.is_authenticated:
        return redirect('guest_side:guest_landing')
    brand = Brand.objects.get(id = id)
    brand.delete()
    messages.info(request,'The status has been deleted successfully')
    return redirect('brands:brands_view')
