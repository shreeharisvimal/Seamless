
from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from cart.models import Coupon
from user_side.models import NewUser
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from products.models import AttributeValue,Atrribute,Product,ProductVariant,Brand
from category_manage.models import Category
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import timedelta
from order_management.models import Payment, Order, OrderItem
from products.models import ProductVariant
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractWeekDay
from django.utils import timezone
from datetime import timedelta
from order_management.models import Payment




app_name = 'admin_side'


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
def admin_login_handler(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        return redirect('user_side:landing')
    if request.user.is_authenticated and request.user.is_superuser :
        return redirect('admin_side:admin_dash_handler')


    
    if request.method == "POST":
        username = request.POST['log_id']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        try:
            if len(password) <4:
                messages.warning(request,'Password must be at least 5 characters long')
                return redirect('admin_side:admin_login_handler')
            
            if not username.is_superuser:
                messages.warning(request,'the user is not an superuser')
                return redirect('admin_side:admin_login_handler')
            
            if username == password:
                messages.warning(request,'the password and the email is same')
                return redirect('admin_side:admin_login_handler')

        except Exception:
            pass
        try:
            user = authenticate(username=username,password=password)
            if user is None:
                messages.warning(request,f"the given details does not match")
            else:       
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_side:admin_dash_handler')
                else:
                    messages.warning(request,f"the given id is not an super user details")
        except Exception:
             pass
                    

    return render(request, 'admin/authentication/login.html')




@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def admin_dash_handler(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    time = datetime.now()
    coup = Coupon.objects.filter(valid_to__lt=time)
    for coupon in coup:
        coupon.is_active = False
        coupon.save()

    current_date = timezone.now() - timedelta(days=6)
    login_date = timezone.now() - timedelta(days=10)
    total_revenue = Payment.objects.filter(payment_status='SUCCESS').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    orders_count = OrderItem.objects.filter(order_status = 'DELIVERED').count() or 0
    product_count = ProductVariant.objects.all().count()
    monthly_sales = Payment.objects.filter(payment_time__month=timezone.now().month, payment_status="SUCCESS").aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    yearly_sales = Payment.objects.filter(payment_time__year=timezone.now().year, payment_status="SUCCESS").aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    user = NewUser.new_manager.filter(is_active = True).count()
    new_member = NewUser.new_manager.filter(start_time__gt=current_date)
    orders = Order.objects.filter(is_complete=True)
    
    weekly_sales_data = get_weekly_sales()
    monthly_sales_data = get_monthly_sales()
    yearly_sales_data = get_yearly_sales()

    # Convert data to string for use in JavaScript
    weekly_sales_str = ",".join(map(str, weekly_sales_data))
    monthly_sales_str = ",".join(map(str, monthly_sales_data))
    yearly_sales_str = ",".join(map(str, yearly_sales_data))

    print(weekly_sales_str)
    print(monthly_sales_str)
    print(yearly_sales_str)


    context = {
        'revenue': total_revenue,
        'orders_count': orders_count,
        'product_count': product_count,
        'weekly_sales_data': weekly_sales_str,
        'monthly_sales_data': monthly_sales_str,
        'yearly_sales_data': yearly_sales_str,
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
        'orders': orders,
        'total_users_count': user,
        'new_members': new_member if new_member else 0,
    }
    return render(request, 'admin/dashboard/index.html', context)

def get_monthly_sales():
    # Query to get monthly sales for the current year
    monthly_sales = Payment.objects.filter(
        payment_time__year=timezone.now().year,
        payment_status="SUCCESS"
    ).annotate(month=ExtractMonth('payment_time')).values('month').annotate(monthly_total=Sum('amount_paid')).order_by('month')

    monthly_sales_values = [0] * 12
    print(monthly_sales)
    for entry in monthly_sales:
        month_index = entry['month'] - 1
        monthly_sales_values[month_index] = entry['monthly_total']

    return monthly_sales_values

def get_yearly_sales():
    yearly_sales = Payment.objects.filter(
       payment_time__year=timezone.now().year,
        payment_status="SUCCESS"
    ).annotate(year=ExtractYear('payment_time')).values('year').annotate(yearly_total=Sum('amount_paid')).order_by('year')

    yearly_sales_values = [0] * 12  # Assuming you want data for each month in a year
    for entry in yearly_sales:
        year_index = entry['year'] - timezone.now().year  # Adjust to get a 0-based index
        yearly_sales_values[year_index] = entry['yearly_total']

    return yearly_sales_values


def get_weekly_sales():
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    print(start_of_week,'\n',end_of_week)
    weekly_sales = Payment.objects.filter(
        payment_time__date__range=[start_of_week, end_of_week],
        payment_status="SUCCESS"
    ).annotate(day_of_week=ExtractWeekDay('payment_time')).values('day_of_week').annotate(weekly_total=Sum('amount_paid')).order_by('day_of_week')
    print(weekly_sales)
    weekly_sales_values = [0] * 7
    for entry in weekly_sales:
  
        adjusted_index = entry['day_of_week'] - 2
        weekly_sales_values[adjusted_index] = entry['weekly_total']

    return weekly_sales_values

@cache_control(no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url='authentication:login_handler')
def admin_user_handler(request):

    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')

    users = NewUser.new_manager.all()
        
    context = {
        'users' :  users
    }
   
    return render(request, 'admin/dashboard/customer.html',context)


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def customer_status(request, user_id):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    
    print(user_id)
    user=get_object_or_404(NewUser, id=user_id)
    print(user)
    if user.is_active:
            user.is_active=False
    
    else:
            user.is_active=True
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def customer_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']
        users = NewUser.new_manager.filter(Q(email__icontains = search_id) | Q(username__icontains = search_id) | Q(phone_number__icontains = search_id))
            
        context = {
            'users' :  users
        }

        return render(request, 'admin/dashboard/customer.html', context)






@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def logout_handler(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('authentication:login_handler')
    print('hello')
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_side:admin_login_handler')


def attribute_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']

        print(search_id)
        print('ahdfjashdfasjklf')
        att = AttributeValue.objects.filter(Q(Attribute_value__icontains=search_id))
        val = Atrribute.objects.filter(attribute_name__icontains=search_id)
        for val in val:
            att = AttributeValue.objects.filter(Q(Attribute = val))

        context = {
            'att' : att,

        }
    return render (request, 'admin/dashboard/product/attribute/attribute_view.html', context)


def variant_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']

        print(search_id)
        print('ahdfjashdfasjklf')
        # variant = ProductVariant.objects.prefetch_related( Prefetch('product',queryset=Product.objects.filter(product_name__icontains = search_id))).filter(
        # Q(model_id__icontains=search_id) | 
        # Q(sale_price__icontains=search_id) |
        # Q(product_varient_slug__icontains=search_id) |
        # Q(updated_at__icontains=search_id) |
        # Q(stock__icontains=search_id) )
        variant = ProductVariant.objects.filter(Q(sale_price__icontains=search_id) |Q(product_varient_slug__icontains=search_id))


        context = {
        'variant' : variant,
        }
    return render (request, 'admin/dashboard/product/variant_view.html', context)




def product_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']
        pro = Product.objects.select_related('product_brand').filter(Q(product_brand__brand_name__icontains = search_id) | Q (product_slug__icontains = search_id)| Q(updated_at__icontains = search_id))
        context = {
            'pro' : pro,
        }
    return render (request, 'admin/dashboard/product/product_view.html', context)


def category_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']

        cat = Category.objects.filter(Q(category_name__icontains =search_id) | Q(slug__icontains=search_id))
    context = {
        'categories': cat
    }
    return render(request, 'admin/dashboard/category.html', context)


def brand_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']
        brand = Brand.objects.filter(Q(brand_name__icontains = search_id))
        context={
            'brands': brand,
        }
    return render(request, 'admin/dashboard/brands/brand.html', context)



def coupon_search(request):
    if request.user.is_authenticated and not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('user_side:landing')
    if request.method=="POST":
        search_id = request.POST['search_id']
        cop = Coupon.objects.filter(Q(code__icontains = search_id) | Q(discount__icontains = search_id))
    context={
        'coupon' : cop
    }
    return render(request, 'admin/dashboard/cart/view_coupon.html',context)