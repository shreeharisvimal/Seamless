
from django.http import Http404
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib import messages
from cart.models import Coupon,Cart_Item,Cart
from account.models import Address
from django.db.models import Q
from decimal import Decimal

# Create your views here.



def order_view(request):
    cart = Cart.objects.get(user = request.user)
    cart_item = Cart_Item.objects.filter(cart = cart.id)
    myuser =request.user
    print(myuser)
    default_billing = None
    default_shipping = None
    billing_address = None
    shipping_address = None
    try:
        default_shipping = Address.objects.filter(Q(is_shipping = True) & Q(is_default = True) & Q( user = request.user))
        default_billing = Address.objects.filter(Q(is_billing = True) & Q(is_default = True) & Q( user = request.user))
        billing_address = Address.objects.filter(Q(is_billing = True) & Q(is_default = False) & Q( user = request.user))
        shipping_address = Address.objects.filter(Q(is_shipping = True) & Q(is_default = False) & Q( user = request.user))
        print(f' the shipping address{shipping_address}')
        print(f'the billing address{billing_address}')
        print(f'the default shipping address{default_shipping}')
        print(f'the default billing address{default_billing}')
    except Exception as e:
        print(f'the error {e}')
    context = {
        'cart' : cart,  
        'cart_item': cart_item,
        'default_billing' :default_billing if default_billing else None ,
        'default_shipping' :default_shipping if default_shipping else None,
        'billing_address':billing_address if billing_address else None,
        'shipping_address':shipping_address if shipping_address else None,
    }
    # try:
    #     context = {
    #     'shipping_address':Address.objects.filter(Q(is_shipping = True) & Q(user= request.user) & ~Q(is_default = True)),
    #     'billing_address':Address.objects.filter(Q(is_billing = True) & Q(user= request.user) & ~Q(is_default = True)),
    #     'default_billing':Address.objects.filter(Q(is_billing = True) & Q(user= request.user) & Q(is_default = True)),
    #     'default_shipping':Address.objects.filter(Q(is_shipping = True) & Q(user= request.user) & Q(is_default = True)),
    #     'all_address':  Address.objects.filter(user = request.user, is_billing=False, is_shipping=False),
    #     }
    #     return render(request, 'user/checkout.html', context)
    # except Exception as e:
    #     print(f'the error is {e}')
    return render(request, 'user/checkout.html',context)


def order_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('user_coupon')
        cart = Cart.objects.get(user = request.user)
        total=cart.sub_total
        
        if cart.coupon is None:
            coupon = Coupon.objects.filter(Q(is_active=True) & Q(code=coupon_code)).first()
            shipping = cart.shipping
            if coupon is None:
                messages.warning(request, f'{coupon_code} is invalid Coupon Code')
                return redirect('cart:view_cart')
            elif coupon is not None:
                cart.total = total 
                cart.total -= coupon.discount if coupon else 0
                cart.total += shipping if shipping else 0
                cart.coupon = coupon
                cart.save()
                return redirect('order:order_view')
            else:
                messages.info(request,'cant you coupons without any cart items')
        else:
            # Handle the case where a user tries to add more than one coupon
            messages.info(request, 'Cannot add more than one coupon')


def order_coupon_delete(request):
    try:
        cart = get_object_or_404(Cart, user = request.user)
        subtotal = cart.sub_total
        off = cart.coupon.discount
        off = Decimal(off)
        shipping = 0
        if subtotal < 200000:
            shipping = (subtotal * Decimal('0.1')) / 100
            print(shipping)
        cart.total = subtotal + shipping if shipping else 0
        cart.coupon = None
        cart.save()
        messages.info(request, 'the coupon has removed')
    except Http404:
        messages.info(request, 'No coupon has been set to remove')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messages.error(request, 'An unexpected error occurred while removing the coupon')
    return redirect('order:order_view')



