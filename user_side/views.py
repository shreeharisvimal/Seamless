from django.shortcuts import  get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from products.models import ProductVariant, Brand
from category_manage.models import Category
from django.db.models import Q
from .models import Wishlist
import math



@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def landing_handler(request):

    if request.user.is_superuser:
        return redirect('admin_side:admin_dash_handler')

    
    pro = ProductVariant.objects.filter(is_active = True)
    cat = Category.objects.filter(is_available = True)
    brand = Brand.objects.filter(is_active = True)
    context = {
        'product' : pro,
        'category' : cat,
        'brand' : brand,
    }  

    return render(request,'user/index.html', context)



@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def product_details(request, id):
    
    pro = ProductVariant.objects.filter(Q(id = id) & Q(is_active=True))
    val = ProductVariant.objects.get(Q(id = id) & Q(is_active=True))
    product = ProductVariant.objects.filter(Q(is_active= True) & ~Q(id=id))
    for prod in product:
            prod.get_variant_name
   

    context = {
        'product' : pro,
        'per' : math.floor((100-((val.sale_price/val.max_price)*100))),
        'prod':product,

    }   
    return render(request, 'user/product_details.html', context)



def add_wishlist(request,id):

    product = ProductVariant.objects.get(pk = id)
    if Wishlist.objects.filter(my_user = request.user, wish_item = product).exists():
        messages.info(request,"This item is already in your wish list")
    else:
        Wishlist.objects.create(my_user = request.user, wish_item = product)
        messages.success(request, "the product added to Wishlist successfully")
        return redirect('user_side:product_details', id = id)
    return redirect('user_side:product_details', id=id) 



def view_wishlist(request):
    wishlist = Wishlist.objects.filter(my_user = request.user)
    user_wishlist = [item.wish_item for item in wishlist]
    
    context = {
        'items' : user_wishlist,
    }
    

    return render(request, 'user/wishlist.html' ,context)


def delete_wishlist(request,id):
    product = Wishlist.objects.get(my_user = request.user, wish_item_id= id)
    messages.warning(request,"item has been removed")
    product.delete()
    return redirect('user_side:view_wishlist')


 
def product_list(request,id=None):
    variant=''
    if id is None:
        all_products = ProductVariant.objects.filter(is_active = True)
        for pro in all_products:
            pro.get_variant_name
    else:
        category = get_object_or_404(Category,id=id)
        pro = category.product_set.all()
        all_products = ProductVariant.objects.filter(Q(product__in=pro) & Q(is_active=True))
        for pro in all_products:
            pro.get_variant_name
    catagory = Category.objects.filter(is_available = True)
    if 'order_by' in request.session:
        all_products= all_products.order_by(request.session['order_by'])
        for pro in all_products:
            pro.get_variant_name

    context = {
        'all_products':all_products,
        'total':all_products.count(),
        'category': catagory,
    }
    
    return render(request, 'user/products_list.html',context)


def product_sort(request,order_by):
    

    request.session['order_by'] = order_by
    return redirect('user_side:product_list')




def category_page(request):
    category = Category.objects.filter(is_available=True)
    context = {
        'cate':category,
    }

    return render(request ,'user/category_page.html' , context)

def all_search(request):
    if request.method=="POST":
        search_id = request.POST['search_id']
        all_products = ProductVariant.objects.filter(Q(is_active = True) & 
        (Q(product_varient_slug__icontains = search_id) | Q(ram__icontains = search_id) | Q(storage__icontains = search_id) | Q(sale_price__icontains = search_id) | Q(color__icontains = search_id)))
        context = {
            'all_products':all_products,
            'total':all_products.count(),
        }
        return render(request, 'user/products_list.html',context)

