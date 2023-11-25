from datetime import datetime as dt
from django.shortcuts import  get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from cart.models import Coupon,Cart_Item,Cart
from django.db.models import Q
from cart.forms import CouponForm
from products.models import ProductVariant
from user_side.models import Wishlist
from decimal import Decimal
def add_coupon(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    form = CouponForm()
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "the coupon has been created")
            return redirect("cart:add_coupon")
        else:   
            messages.warning(request,"the date format is not valid or the form is not valid")
    else:
        form = CouponForm()
    return render (request, 'admin/dashboard/cart/coupon.html',{'form':form})


def view_coupon(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    time = dt.now()
    coup = Coupon.objects.filter(valid_to__lt = time)
    for coupon in coup:
        coupon.is_active = False
        coupon.save()
    print(coupon.is_active)


    coup = Coupon.objects.filter(valid_to__exact= dt.now())
    coup.delete()
    context={
        'coupon' : Coupon.objects.all(),
    }

    return render(request, 'admin/dashboard/cart/view_coupon.html',context)

def status_coupon(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    if request.method=="POST":
        coupon = Coupon.objects.get(id = id)
        print(coupon)
        if coupon.is_active == True:
            coupon.is_active = False
            coupon.save()
            messages.info(request,f"the coupon {coupon} is set to INACTIVE")
        else:
            coupon.is_active = True
            coupon.save()
            messages.info(request,f"the coupon {coupon} is set to ACTIVE")

    return redirect('cart:view_coupon')


def delete_coupon(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    if request.method == "POST":
        try:
            coupon = Coupon.objects.get(id=id)
            coupon.delete()
            messages.info(request,f'The coupon has been deleted {coupon}')
        except:
            pass
    return redirect('cart:view_coupon')


def view_cart(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    
    cart, check_cart = Cart.objects.get_or_create(user=request.user)
    cart_items = Cart_Item.objects.filter(cart=cart)    
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    shipping = 0
    total = Decimal(0)
 #checking if the user can get free delivery 
    if subtotal < 200000:
        shipping = (subtotal * Decimal('0.1')) / 100
        total = subtotal + shipping
        # request.session['shipping'] = shipping
    else:
        total = subtotal
    off = 0

    if cart.coupon is not None:
        code = cart.coupon
        total -= code.discount
        off = code.discount
    if request.method == 'POST':
        coupon_code = request.POST.get('user_coupon')
        if cart.coupon is None:
            
            code = Coupon.objects.filter(Q(is_active=True) & Q(code=coupon_code)).first()
            if code is None:
                messages.warning(request, f'{coupon_code} is invalid Coupon Code')
                return redirect('cart:view_cart')

            elif total !=0:
                total = total - code.discount
                off = code.discount
                cart.sub_total = total
                cart.coupon = code
                cart.save()
            else:
                messages.info(request,'cant you coupons without any cart items')

        else:
            # Handle the case where a user tries to add more than one coupon
            messages.info(request, 'Cannot add more than one coupon')

    # Check if the cart is empty and update the Cart model
    if not cart_items:
        cart.sub_total = None
        cart.coupon = None
        cart.save()
    context = {
        'item': cart_items,
        'pro_subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'off': off,
        'cart': Cart.objects.filter(user=request.user),
    }
    return render(request, 'user/cart.html', context)



def add_cart(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    product = get_object_or_404(ProductVariant, id=id)
    cart,check_cart = Cart.objects.get_or_create(user = request.user)
    cart_item,check_cart_item = Cart_Item.objects.get_or_create(cart = cart, product = product)
    wish = Wishlist.objects.filter(Q(my_user = request.user) & Q(wish_item=product))
    if wish:
        wish.delete()
    if not check_cart_item:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')




def delete_cart(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')

    cart_item = Cart_Item.objects.filter(id = id)
    if cart_item:
        cart_item.delete()
        messages.info(request, f"the item has been deleted from cart")
    cart = get_object_or_404(Cart, user = request.user)
    if not cart_item:
        cart.sub_total = None
        cart.coupon = None
        cart.save()

    return redirect('cart:view_cart')

def item_plus(request,id):
    cart = get_object_or_404(Cart, user = request.user)
    cart_item = Cart_Item.objects.filter(cart=cart, id=id)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_item)
    for item in cart_item:
        item.quantity += 1
        item.save()
    coupon = cart.coupon
    cart_item_sum = Cart_Item.objects.filter(cart=cart)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_item_sum)
    shipping = 0
    if subtotal < 200000:
        shipping = (subtotal * Decimal('0.1')) / 100
    subtotal += shipping if shipping else 0 
    subtotal -= coupon.discount if coupon else 0
    if not cart_item:
        cart.sub_total = None
        cart.coupon = None
        cart.save()
    cart.sub_total=subtotal
    cart.save()
    return redirect('cart:view_cart')



def item_minus(request,id):
    cart = get_object_or_404(Cart, user = request.user)
    cart_item = Cart_Item.objects.filter(cart=cart, id=id)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_item)
    for item in cart_item:
        item.quantity -= 1
        item.save()
    if item.quantity < 1:
        cart_item.delete()
    coupon = cart.coupon
    cart_item_sum = Cart_Item.objects.filter(cart=cart)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_item_sum)
    shipping = 0
    if subtotal < 200000:
        shipping = (subtotal * Decimal('0.1')) / 100
    subtotal += shipping if shipping else 0 
    subtotal -= coupon.discount if coupon else 0
    if not cart_item:
        cart.sub_total = None
        cart.coupon = None
        cart.save()
    cart.sub_total=subtotal
    cart.save()
    return redirect('cart:view_cart')


def remove_coupon(request,id):
    cart = get_object_or_404(Cart, user = request.user)
    off = cart.coupon.discount
    off = Decimal(off)
    cart.sub_total += off
    cart.coupon = None
    cart.save()
    messages.info(request, 'the coupon has removed')
    return redirect('cart:view_cart')

def clear_cart(request):
    cart = get_object_or_404(Cart, user = request.user)
    cart_item = Cart_Item.objects.filter(cart=cart)
    cart_item.delete()
    cart.coupon = None
    cart.save()
    return redirect('cart:view_cart')