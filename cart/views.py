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
from django.http import JsonResponse
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
    cart_items = Cart_Item.objects.filter(cart=cart).order_by('id')
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    shipping = 0
    total = Decimal(subtotal)
    off = 0

    # checking if the user can get free delivery
    if subtotal < 200000:
        shipping = (subtotal * Decimal('0.1')) / 100
        total += shipping  # Include shipping in the total

        # Handle coupon application for the first time
    if request.method == 'POST':
        coupon_code = request.POST.get('user_coupon')
        code = Coupon.objects.filter(Q(is_active=True) & Q(code=coupon_code)).first()

        if code is None:
            messages.warning(request, f'{coupon_code} is an invalid Coupon Code')
        elif total != 0:
            cart.sub_total = subtotal
            cart.total = total - code.discount
            off = code.discount
            cart.coupon = code
            cart.shipping = shipping
            cart.save()
            messages.success(request,'the Coupon have been added to the cart')
            return redirect('cart:view_cart')

    # Check if the cart is empty and update the Cart model
    if not cart_items:
        cart.total = None
        cart.sub_total = None
        cart.coupon = None
        cart.shipping = None
        cart.save()
        messages.info(request,'Cart is Running on Low')
        
    context = {
        'item': cart_items,  # Renamed 'item' to 'items' for clarity
        'pro_subtotal': cart.sub_total if cart.sub_total else subtotal,
        'shipping': cart.shipping if cart.shipping else shipping,
        'total': cart.total if cart.total else total,
        'off': cart.coupon.discount if cart.coupon else off,
        'cart': Cart.objects.filter(user=request.user),
    }
    return render(request, 'user/cart.html', context)




def add_cart(request, id=None):
    if request.user.is_superuser:
        return JsonResponse({'error': 'User not authorized'}, status=403)

    product_quantity = int(request.POST.get('prod_qty')) if request.POST.get('prod_qty') else 1
    product_id = int(request.POST.get('prod_id')) if request.POST.get('prod_id') else id
    product = get_object_or_404(ProductVariant, id = product_id)
    cart, check_cart = Cart.objects.get_or_create(user=request.user)
    try:
        item_check = Cart_Item.objects.get(cart=cart, product=product)
    
        if product_quantity > product.stock :
            messages.warning(request, 'cant add that many due to stock insufficient')
            return redirect('cart:view_cart')
        elif item_check.quantity + product_quantity > product.stock:
             
            messages.warning(request, 'cant add that many due to stock insufficient')
            return redirect('cart:view_cart')
        else:
            
            item_check.quantity += product_quantity if product_quantity else 1
            item_check.save()
            cart_item = Cart_Item.objects.filter(cart = cart)
            subtotal = sum(item.product.sale_price * item.quantity for item in cart_item)
            coupon = cart.coupon
            shipping = 0
            if subtotal <200000:
                shipping = (subtotal * Decimal('0.1')) / 100
            cart.sub_total = subtotal
            cart.coupon = coupon
            subtotal -= coupon.discount if coupon else 0
            cart.total = subtotal if subtotal else 0
            cart.total += shipping if shipping else 0
            cart.shipping = shipping if shipping else 0
            cart.save()
            messages.success(request, 'The product is in the cart')
            return redirect("cart:view_cart")
    except Cart_Item.DoesNotExist:
        Cart_Item.objects.create(cart=cart, product=product, quantity=product_quantity if product_quantity else 1)
        cart_item = Cart_Item.objects.filter(cart = cart)
        subtotal = sum(item.product.sale_price * item.quantity for item in cart_item)
        coupon = cart.coupon
        shipping = 0
        if subtotal <200000:
            shipping = (subtotal * Decimal('0.1')) / 100
        cart.sub_total = subtotal
        cart.coupon = coupon
        subtotal -= coupon.discount if coupon else 0
        cart.total = subtotal if subtotal else 0
        cart.total += shipping if shipping else 0
        cart.shipping = shipping if shipping else 0
        cart.save()
        messages.success(request, 'The item has been added to the cart')
        wish = Wishlist.objects.filter(Q(my_user=request.user) & Q(wish_item=product))
        if wish:
            wish.delete()

        return redirect("cart:view_cart")





def delete_cart(request,id):
    cart_item = Cart_Item.objects.filter(id = id)
    if cart_item:
        cart_item.delete()
        messages.info(request, f"the item has been deleted from cart")
    myCart =Cart.objects.get(user = request.user)
    del_cart = Cart_Item.objects.filter(cart =myCart)
    coupon = myCart.coupon
    subtotal = sum(item.product.sale_price * item.quantity for item in del_cart) 
    product_per_price = subtotal
    shipping = Decimal(0)
    if subtotal < 200000:
        shipping = (subtotal * Decimal('0.1'))/100
    subtotal -= coupon.discount if coupon else 0
    myCart.sub_total = product_per_price if product_per_price else 0
    myCart.total = subtotal
    myCart.total += shipping if shipping else 0
    myCart.shipping = shipping if shipping else 0
    myCart.save()
    if del_cart is None:
        myCart.total = None
        myCart.sub_total = None
        myCart.coupon = None
        myCart.shipping = None
    return redirect('cart:view_cart')

def item_plus(request):
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            cart = get_object_or_404(Cart, user = request.user)
            id = request.POST.get('cart_id')
            cart_item = get_object_or_404(Cart_Item, cart = cart, id = id)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
            subtotal = Decimal(0)   
            coupon = cart.coupon
            cart_item = Cart_Item.objects.filter(cart = cart)
            subtotal = sum(item.product.sale_price * item.quantity for item in cart_item) 
            product_per_price = subtotal
            shipping = Decimal(0)
            if subtotal < 200000:
                shipping = (subtotal * Decimal('0.1'))/100
        
            subtotal -= coupon.discount if coupon else 0
            cart.sub_total = product_per_price if product_per_price else 0
            cart.total = subtotal
            cart.total += shipping if shipping else 0
            cart.shipping = shipping if shipping else 0
            cart.save()
            quantity = [{'id': item.id, 'quantity': item.quantity} for item in cart_item]
            data = {
                'quantity' : quantity,
                'subtotal' : f'₹ {product_per_price: .2f}',
                'shipping': f'₹ {shipping:.2f}' if shipping else 'Free Shipping',
                'total': f'₹ {cart.total:.2f}',
                'off': f'₹ {coupon.discount:.2f}' if coupon else '₹ 0.00',
            }
            return JsonResponse(data)
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {str(e)}")
            messages.info(request, 'Cant add more product quantity than its products stock')
    return JsonResponse({'error': 'Invalid request'}, status=400)
      

def item_minus(request):
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            cart = get_object_or_404(Cart, user = request.user)
            id = request.POST.get('cart_id')
            cart_item = get_object_or_404(Cart_Item, cart = cart, id = id)
            print(cart_item.product.stock)
            print(cart_item.quantity)
            if cart_item.quantity > 1 and cart_item.quantity <= cart_item.product.stock:
                cart_item.quantity -= 1
                cart_item.save()


            subtotal = Decimal(0)   
            coupon = cart.coupon
            cart_item = Cart_Item.objects.filter(cart = cart)
            subtotal = sum(item.product.sale_price * item.quantity for item in cart_item)   
            cart.sub_total = subtotal
            product_per_price = subtotal
            shipping = Decimal(0)
            if subtotal < 200000:
                shipping = (subtotal * Decimal('0.1'))/100
            subtotal -= coupon.discount if coupon else 0
            cart.sub_total = product_per_price if product_per_price else 0
            cart.total = subtotal
            cart.total += shipping if shipping else 0
            cart.shipping = shipping if shipping else 0
            cart.save()
            quantity = [{'id': item.id, 'quantity': item.quantity} for item in cart_item]
            data = {
                'quantity' : quantity,
                'subtotal' : f'₹ {product_per_price: .2f}',
                'shipping': f'₹ {shipping:.2f}' if shipping else 'Free Shipping',
                'total': f'₹ {cart.total:.2f}',
                'off': f'₹ {coupon.discount:.2f}' if coupon else '₹ 0.00',
            }
            return JsonResponse(data)
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

def remove_coupon(request):
    try:
        cart = get_object_or_404(Cart, user = request.user)
        off = cart.coupon.discount
        off = Decimal(off)
        cart.total += off
        cart.coupon = None
        cart.save()
        messages.info(request, 'the coupon has removed')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messages.info(request, 'No coupon has been Used to remove')
    return redirect('cart:view_cart')

def clear_cart(request):
    cart = get_object_or_404(Cart, user = request.user)
    cart_item = Cart_Item.objects.filter(cart=cart)
    cart_item.delete()
    cart.coupon = None
    cart.save()
    messages.info(request,'all the cart items have been deleted')
    return redirect('cart:view_cart')