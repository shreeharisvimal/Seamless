from django.conf import settings
import razorpay
import uuid
from django.http import Http404, JsonResponse
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from cart.models import Coupon,Cart_Item,Cart
from account.models import Address
from django.db.models import Q
from decimal import Decimal
from products.models import ProductVariant
from order_management.models import Order,OrderItem,Payment
from account.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
                return redirect('order:order_view')
            elif coupon is not None:
                cart.total = total 
                cart.total -= coupon.discount if coupon else 0
                cart.total += shipping if shipping else 0
                cart.coupon = coupon
                cart.save()
                messages.success(request,'the Coupon has been added Sucessfully')
                return redirect('order:order_view')
            else:
                messages.info(request,'cant you coupons without any cart items')
        else:
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

def place_order(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            shipping_address_id = request.POST.get('shipping')
            billing_address_id = request.POST.get('billing')
            if not shipping_address_id or not billing_address_id:
                messages.error(request, 'Please select both address')
                return JsonResponse({'success': False, 'message': 'Error placing order: Select address for delivery'})
            shipping =Address.objects.get(id=(shipping_address_id))
            billing =Address.objects.get(id=(billing_address_id))
            cart = Cart.objects.get(user = request.user)
            cart_item = Cart_Item.objects.filter(cart = cart)

            # payment_mode = request.POST.get('payment_choice')
            payment_mode = request.POST['payment_select']
            print(f'hdfsakjdfnas paymetn mode {payment_mode}')
            
            if payment_mode == "exampleRadios6":
                payment_mode = 'COD'
            else:
                messages.warning(request,'select an valid payment option')
            payment_maker = Payment.objects.create(
            user=request.user,
            payment_method = payment_mode,
            payment_status = 'PENDING',
            amount_paid = cart.total,
            )
            order_item = None
            coupon = None
            try:
                if cart.coupon:
                    coupon = Coupon.objects.get(id=cart.coupon.id)
                # Create a new order instance
                new_order =Order.objects.create(
                user=request.user,
                payment_details = payment_maker,
                shipping_address = shipping,
                billing_address = billing,
                order_total = cart.total,
                order_subtotal = cart.sub_total,
                order_shipping = cart.shipping,
                order_coupon = coupon if coupon else None,
                )
                request.session['order'] = new_order.order_number
                cart.coupon = None 
                cart.save()
                print(coupon)
            except Exception as e:
                print(f' the error {e}')
            for cart_item in cart_item:
                product = ProductVariant.objects.get(id=cart_item.product.id)
                uu_order_id = int(uuid.uuid4().hex[:8],16)
                uu_order_id = f"#{uu_order_id}"

                order_item, _ = OrderItem.objects.get_or_create(
                    user=request.user, 
                    order_product=product,
                    order_item_id = uu_order_id,
                    quantity=cart_item.quantity, 
                    product_price=cart_item.product.sale_price, 
                    payment_details=payment_maker,
                    order = new_order,
                    order_status = 'PROCESSING',
                    )
                product.stock -= cart_item.quantity
                product.save()
                order_item.save()
                cart_item.delete()
            
        except KeyError as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: the error is {str(e)}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
        
    return redirect('order:order_status')



def order_user_view(request):
    order = Order.objects.filter(user = request.user).order_by('-order_time')
    context = {
        'order':order
    }

    return render(request, 'user/order/order_list.html',context)
    



def order_details(request):

    shipping=None
    billing=None
    order_item=None
    order=None
    user_details=None

    try:
        new_order = request.session.get('order')
        print(f'the payment id  {new_order}')
        order = Order.objects.get(order_number = new_order)
        order_item = OrderItem.objects.filter(order = order)
        user_details = UserProfile.objects.get(user = request.user)
        shipping = Address.objects.get(id=order.shipping_address.id)
        billing = Address.objects.get(id=order.billing_address.id)
        print(f"the order item MY ITEM {order_item}")
        print(f'the payment id  {new_order}')
        print('the dfdsahjflkasfsfasfasfasff')
    except Exception as e:
        print(f'the error is in {e}')
    print(f"the order item MY ITEM {order_item}")
    print('the dfdsahjflkasfsfasfasfasff')
    context = {
        'order_item':order_item,
        'order':order,
        'profile':user_details,
        'billing':billing,
        'shipping':shipping,
    }
    messages.success(request, 'Hooray the order have been placed')

    try:
        print(f"the order itemid in try block {order_item}")
        print('the dfdsahjflkasfsfasfasfasff')
        messages.success(request, 'This is the Invoice of Your purchase and a copy will be also send to the email')
        mail_content = render_to_string('user/order/order_invoice.html',context)
        subject = 'Order Invoice Seamless'
        from_email = 'yourseamlesslife@gmail.com'
        to_email = [user_details.user.email]
        send_mail(
        subject,
        strip_tags(mail_content),  # Plain text version
        from_email,
        to_email,
        html_message=mail_content,  # HTML version
        )
        data = {'success': True}
        return JsonResponse(data)
    except Exception as e:
        print(f'the error is that {e}')
        data = {'success': False}
        return JsonResponse(data)



def invoice_showing(request):
    shipping=None
    billing=None
    order_item=None
    order=None
    user_details=None

    try:
        new_order = request.session.get('order')
        print(f'the payment id  {new_order}')
        order = Order.objects.get(order_number = new_order)
        order_item = OrderItem.objects.filter(order = order)
        user_details = UserProfile.objects.get(user = request.user)
        shipping = Address.objects.get(id=order.shipping_address.id)
        billing = Address.objects.get(id=order.billing_address.id)
        print(f"the order item MY ITEM {order_item}")
        print(f'the payment id  {new_order}')
        print('the dfdsahjflkasfsfasfasfasff')
    except Exception as e:
        print(f'the error is in {e}')
    print(f"the order item MY ITEM {order_item}")
    print('the dfdsahjflkasfsfasfasfasff')
    context = {
        'order_item':order_item,
        'order':order,
        'profile':user_details,
        'billing':billing,
        'shipping':shipping,
    }
    messages.success(request, 'Hooray the order have been placed')
    return render(request,'user/order/order_invoice.html',context)


def order_listing(request,id):  
    order = Order.objects.get(order_number = id)
    order_item = OrderItem.objects.filter(order = order)
    user_details = UserProfile.objects.get(user = request.user)

    print(f"the order item {order_item}")
    context = {
        'order':order,
        'order_item':order_item,
        'profile':user_details,
    }

    return render(request, 'user/order/order_item_listing_user.html',context)


def cancel_order(request,id):
    print(f' ndfk the error {id}')
    item_id = id
    order_item = OrderItem.objects.get(id = item_id)
    Product = ProductVariant.objects.get(id = order_item.order_product.id)

    context = {
        'order_item':order_item,
        'Product':Product,
    }
    return render(request, 'user/order/order_cancel.html',context)

def cancel_order_request(request,id):
    print(f' ndfkasndfk the error {id}')
    order_item = OrderItem.objects.get(id = id)
    Product = ProductVariant.objects.get(id = order_item.order_product.id)
    user_details = get_object_or_404(UserProfile, user = request.user)
    print(Product)
    if request.method =="POST":
        try:
            reason = request.POST['reason']
            if reason is None:
                messages.warning(request,'Reason for cancellation is Must')
            order_item.cancel_reason = reason
            order_item.order_status = 'CANCELLED'
            Product.stock += int(order_item.quantity)
            order_item.order.order_total -= (int(order_item.product_price) * int(order_item.quantity))
            print((int(order_item.product_price) * int(order_item.quantity)))
            print(order_item.order.order_total)
            order_item.order.save()
            print(f'the final saving {order_item.order.order_total}')
            order_item.save()
            if order_item.order.order_total < 0:
                order_item.order.order_total = 0
                order_item.order.save()
            Product.save()
            context = {
                'order_item':order_item,
                'profile':user_details, 
                'Product':Product,
            }
            try:
                mail_content = render_to_string('user/order/order_cancel_invoice.html', context)
                subject = 'Order Cancel request Accepted '
                from_email= 'yourseamlesslife@gmail.com'
                to_email = [user_details.user.email]
                send_mail(
                    subject,
                    strip_tags(mail_content),
                    from_email,
                    to_email,
                    html_message=mail_content,
                )
            except Exception as e:
                print(f'the error is {e}')
            
            messages.info(request,'The order has been cancelled soon you will recive confirmation mail')
            return redirect('order:order_listing')
        except Exception as e:
            print(f'an error has been occured {e}')
            return redirect('order:order_user_view')
    return render(request, 'user/order/order_cancel.html')



def admin_order_view(request):
    order = Order.objects.all().order_by('-order_time')
    context ={
        'order':order,
    }
    return render(request, 'admin/dashboard/order/order_view.html',context)


def admin_order_item_view(request, id):
    order = Order.objects.get(order_number=id)
    order_item = OrderItem.objects.filter(order=order)
    
    context={
        'order_item':order_item,
        'order':order
    }

    return render(request, 'admin/dashboard/order/order_item_view.html',context)



def admin_order_item_details(request, id):
    order_no = id
    order_item = OrderItem.objects.get(id=order_no)
    print(order_item)
    context={
        'order_item':order_item,
    }
    return render(request, 'admin/dashboard/order/order_item_details.html',context)

def admin_order_status(request):
    order_id = None
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            select_status = request.POST.get('status')
            order_item = get_object_or_404(OrderItem, order_item_id = order_id)
            order_item.order_status = select_status
            if select_status == "CANCELLED":
                order_item.order.order_total -= (int(order_item.product_price) * int(order_item.quantity))
                if order_item.order.order_total < 0:
                    order_item.order.order_total = 0
                order_item.order.save()
            order_item.save()
            data = {'success': True}
            return JsonResponse(data)
        except Exception as e:
            print(f'order change: {e}')
            data = {'success': False}
            return JsonResponse(data)

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def admin_order_status_all(request):
    order_id = None
    order = None
    select_status = None
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            select_status = request.POST.get('status')
            order = get_object_or_404(Order, order_number=order_id)
            order_item = OrderItem.objects.filter(Q(order=order) & ~Q(order_status='CANCELLED'))
            for item in order_item:
                print('inside the looop')
                item.order_status = select_status
                if select_status == 'CANCELLED':
                    order.order_total -= (int(item.product_price) * int(item.quantity))
                order.save()
                item.save()
                if order.order_total < 0:
                    order.order_total = 0
                    order.save()
                print('inside the all cancel ) setting if')
                messages.info(request, f'The order Number {order_id} status has been changed')
            data = {'success': True}
            return JsonResponse(data)
        except Exception as e:
            print(f'The error is in admin all order change: {e}')
            data = {'success': False}
            return JsonResponse(data)
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def user_order_tracking(request):
    if request.method =="POST":
        order_item_id = request.POST.get('order_item_id')
        payment_id = request.POST.get('payment_id')
        if order_item_id and payment_id:
            order_item = OrderItem.objects.get(id=order_item_id, payment_details = payment_id)
            order = order_item.order
            context = {
                'order_item':order_item,
                'order':order
            }
            mail = render_to_string('user/order/order_tracking', context)
            subject = 'Your Order tracking request'
            from_email = 'yourseamlesslife@gmail.com'
            to_email = [request.user.email]
            send_mail(
                subject,
                strip_tags(mail),
                from_email,
                to_email,
                html_message=mail,
            )
        messages.success(request,'The Order tracking details has been sent to mail')
    return redirect('order:order_listing')



def pay_with_razor(request):
    cart = Cart.objects.get(user = request.user)
    profile = UserProfile.objects.get(user = request.user)
    shipping = None
    billing= None
    order_response= None
    try:
        cart = Cart.objects.get(user = request.user)
        cart_item = Cart_Item.objects.filter(cart = cart)
        # razor_payment_id = request.POST.get('razorpay_payment_id')
        print(f"{shipping}    asdfasdfasfasd       asdfasdfasfasd     {request.POST.get('shipping')}")
        print(f"{billing}   asdfasdfasfasd      asdfasdfasfasd    {request.POST.get('billing')}")
        shipping = get_object_or_404(Address, id = request.POST.get('shipping'))
        billing = get_object_or_404(Address, id = request.POST.get('billing'))
        user_details = UserProfile.objects.get(user = request.user)
        if shipping is None or billing is None:
            messages.success(request, 'Please select your Both address')
            return JsonResponse(ValueError)
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        order_response = client.order.create({
            'amount' : int(float(cart.total)*100),
            'currency' : "INR",
            'receipt' : f"#{cart.id}_{uuid.uuid4().hex[:8]}",
            'payment_capture' : 1,
        })
        payment_maker = Payment.objects.create(
            user=request.user,
            razorpay_payment_id = order_response["id"],
            payment_method = 'RazorPay',
            payment_status = 'PENDING',
            amount_paid = cart.total,
            )
        print(payment_maker)
        order_item = None
        coupon = None
        product = None

        if cart.coupon:
            coupon = Coupon.objects.get(id = cart.coupon.id)
        new_order =Order.objects.create(
        user=request.user,
        payment_details = payment_maker,
        shipping_address = shipping,
        billing_address = billing,
        order_total = cart.total,
        order_subtotal = cart.sub_total,
        order_shipping = cart.shipping,
        order_coupon = coupon if coupon else None,
        )
        print('hello in the after order create')
        request.session['order'] = new_order.order_number
        print(request.session.get('order'))
        cart.coupon = None 
        cart.save()
        for cart_item in cart_item:
            print(product)
            product = ProductVariant.objects.get(id = cart_item.product.id)
            print(product)
            uu_id = int(uuid.uuid4().hex[:8],16)
            uu_id = f'#{uu_id}'

            order_item, _ = OrderItem.objects.get_or_create(
            user=request.user, 
            order_product=product,
            order_item_id = uu_id,
            quantity=cart_item.quantity, 
            product_price=cart_item.product.sale_price, 
            payment_details=payment_maker,
            order = new_order,
            order_status = 'PROCESSING',
            )
            product.stock -= cart_item.quantity
            product.save()
            order_item.save()
            cart_item.delete()

    except Exception as e:
        print(f" the error is  {e}")
    context = {
    'order_item':OrderItem.objects.filter(order = new_order),   
    'order':new_order,
    'profile':user_details,
    'billing':billing,
    'shipping':shipping,
    }
    mail_content = render_to_string('user/order/order_invoice.html',context)
    subject = 'Order Invoice Seamless'
    from_email = 'yourseamlesslife@gmail.com'
    to_email = [user_details.user.email]
    send_mail(
    subject,
    strip_tags(mail_content),  # Plain text version
    from_email,
    to_email,
    html_message=mail_content,  # HTML version
    )
    return JsonResponse({
        'full_name':profile.full_name,
        'email':profile.email,
        'phone_number':profile.phone_number,
        'order_response':{
            'amount':order_response.get('amount'),
            'order_id': order_response.get('id'),
        },
    })


