from decimal import Decimal
from django.shortcuts import  get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from products.models import ProductVariant, Brand, Product
from category_manage.models import Category
from django.db.models import Q

from cart.models import Cart, Cart_Item
from .models import Wishlist
import math
from account.models import UserProfile 
from django.http import JsonResponse
from review_management.models import review
import json


@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def landing_handler(request):

    if request.user.is_superuser:
        return redirect('admin_side:admin_dash_handler')

    try:
        pro = ProductVariant.objects.filter(is_active = True)
        cat = Category.objects.filter(is_available = True)
        brand = Brand.objects.filter(is_active = True)
        
        context = {
            'product' : pro,
            'category' : cat,
            'brand' : brand,
        }  
    except Exception as e:
        print(f'the error is {e}')
    return render(request,'user/index.html', context)



@cache_control(no_cache=True, must_revalidate=True, max_age=0)
def product_details(request, id):
    mean = Decimal(0.0)
    print(id)
    pro = ProductVariant.objects.filter(Q(id = id) & Q(is_active=True))
    val = ProductVariant.objects.get(Q(id = id) & Q(is_active=True))
    product = ProductVariant.objects.filter(Q(is_active= True) & ~Q(id=id))
    rev = review.objects.filter(product = id)
    for prod in product:
            prod.get_variant_name
    try:    
        print(rev)
        if rev.exists():
            mean = sum(review.stars for review in rev) / len(rev)
            print(mean)
            mean = round(mean, 2)
            print("Mean Rating:", mean)
    except Exception as e:
        print(e)
    context = {
        'stars' : {
            'mean':mean,
            'total':rev.count(),
            'one': round((review.objects.filter(stars=1, product = id).count() / max(1, rev.count())) * 100),
            'two': round((review.objects.filter(stars=2, product = id).count() / max(1, rev.count())) * 100),
            'three': round((review.objects.filter(stars=3, product = id).count() / max(1, rev.count())) * 100),
            'four': round((review.objects.filter(stars=4, product = id).count() / max(1, rev.count())) * 100),
            'five': round((review.objects.filter(stars=5, product = id).count() / max(1, rev.count())) * 100),
        },
        'review': rev,
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
        return redirect('user_side:product_list')
    return redirect('user_side:product_details', id=id) 



def view_wishlist(request):
    wishlist = Wishlist.objects.filter(my_user = request.user)
    user_wishlist = [item.wish_item for item in wishlist]
    
    context = {
        'items' : user_wishlist,
    }
    

    return render(request, 'user/wishlist.html' ,context)


def search(request):
    search_id = request.POST.get('search_term')
    print(search_id)
    if search_id:
        all_products = ProductVariant.objects.filter(
            Q(is_active=True) &
            (Q(product_varient_slug__icontains=search_id) |
            Q(ram__icontains=search_id) |
            Q(storage__icontains=search_id) |
            Q(sale_price__icontains=search_id) |
            Q(color__icontains=search_id))
        ).values()
        if all_products:
            return JsonResponse({ 'data': list(all_products)})
        else:
            return JsonResponse({'success': 'Nothing', 'message': 'No matching products'})
    else:
        return JsonResponse({'success': 'Nothing'})




def delete_wishlist(request,id):
    product = Wishlist.objects.get(my_user = request.user, wish_item_id= id)
    messages.warning(request,"item has been removed")
    product.delete()
    return redirect('user_side:view_wishlist')


 
def product_list(request,id=None):
    Mycategory = None
    myProducts = []
    if request.user.is_authenticated:
        cart_id = Cart.objects.get(user = request.user)
        request.session['cart_id'] = cart_id.pk

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
    try:
        for cart_items in Cart_Item.objects.filter(cart = cart_id.pk):
            Mycategory = cart_items.product.product.product_catg
            for prod in Product.objects.filter(product_catg = Mycategory):
                for variant in ProductVariant.objects.filter(product = prod):
                    if cart_items.product.pk != variant.pk:
                        if cart_items.product not in myProducts:
                            myProducts.append(variant)
                
        for wish in Wishlist.objects.filter(my_user = request.user):
            for prod in Product.objects.filter(product_catg = wish.wish_item.product.product_catg):
                for variant in ProductVariant.objects.filter(product = prod):
                    if wish.wish_item.pk != variant.pk:
                        if wish.wish_item not in myProducts:
                            myProducts.append(variant)
       
    except Exception as e:
        print(f'the error is that {e}')
    context = {
        'all_products':all_products,
        'total':all_products.count(),
        'category': catagory,
        'recommend_products': myProducts[:6] if myProducts else None,

    }
    
    return render(request, 'user/products_list.html',context)


def product_sort(request,order_by):
    

    request.session['order_by'] = order_by
    return redirect('user_side:product_list')


def product_filter(request):
    min_price = None
    max_price = None
    myProducts  = []
    if request.method == "POST":
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        print(min_price)
        print(max_price)
        
        if max_price and min_price:
            for cart_items in Cart_Item.objects.filter(cart = request.session.get('cart_id')  ):
                Mycategory = cart_items.product.product.product_catg
                for prod in Product.objects.filter(product_catg = Mycategory):
                    for variant in ProductVariant.objects.filter(product = prod):
                        myProducts.append(variant)

            all_products = ProductVariant.objects.filter(Q(sale_price__gte = min_price) & Q(sale_price__lte = max_price))

            context  ={
                'all_products' : all_products,
                'recommend_products': myProducts[:6] if myProducts else None,

            }
        
            return render(request, 'user/products_list.html',context)
        else:
            messages.error(request,"Please Enter Both The Values")
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
    
def change_profile_image(request):
    acc_user = UserProfile.objects.get(user = request.user)
    try:
        if request.FILES.get('Profile_img'):
            acc_user.profile_pic = request.FILES.get('Profile_img')
            acc_user.save()
            data = {
                'success': True,
            }
        return JsonResponse(data)
    except Exception as e:
        pass