from django.shortcuts import  get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from products.models import ProductVariant, Brand
from wallet.models import Wallet, SeamPay
from category_manage.models import Category
from django.db.models import Q
import math

# Create your views here.






def wallet_view(request):
    seam =  SeamPay.objects.get(user = request.user)
    wallet = Wallet.objects.filter(user = request.user, seampay = seam).order_by('-created_at')
    context = {
        'wallet': wallet,
        'seam':seam,
    }
    return render(request, 'user/dashboard/wallet.html', context)

def credit(amount, order_item, user):
    print('hi')
    try:
        amount = amount
        order_item = order_item
        seam, check = SeamPay.objects.get_or_create(user = user)
        print('in the has attri checking')
        Wallet.objects.get_or_create(
            user = user,
            seampay = seam,
            payment = order_item.payment_details,
            order_id = order_item.order.order_number,
            order_item = order_item,
            amount = amount,
            is_debit = False,
        )
        seam.balance +=amount
        seam.save()

    except Exception as e:
        print(f'the error is that which is {e}')

    

def seampay_razor(amount, order_item, user):
    seam = get_object_or_404(SeamPay, user =user)

    Wallet.objects.get_or_create(
        user = user,
        seampay = seam,
        payment = order_item.payment_details,
        order_id = order_item.order.order_number,
        order_item = order_item,
        amount = amount,
        is_debit = True,
    )
    seam.balance = 0
    seam.save()

    



def seampay(total, order_item, user):
    check = None
    main_balance = None
    seam = get_object_or_404(SeamPay, user =user)
    print(f'the total from tthe seam getted {total}')
    check = seam.balance
    main_balance =  seam.balance - total
    check -= main_balance
    seam.balance = main_balance
    print('if seam.balance > total:   in this if conditrion')
    print(f'from the if  case returning the values the main {main_balance} and the total {total}')
    Wallet.objects.get_or_create(
    user = user,
    seampay = seam,
    payment = order_item.payment_details,
    order_id = order_item.order.order_number,
    order_item = order_item,
    amount = total,
    is_debit = True,
)
    seam.save()
    print(f'the main from the function {main_balance}')
    


    
    
