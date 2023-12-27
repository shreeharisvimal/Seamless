import math
from django.shortcuts import  get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from products.models import ProductVariant, Brand
from wallet.models import Wallet, SeamPay
from category_manage.models import Category
from django.db.models import Q
from order_management.models import OrderItem
from .models import review


def review_view(request,id):
    order_item = OrderItem.objects.get(pk = id)
    rev = review.objects.filter(product =order_item.order_product.pk)
    val = ProductVariant.objects.get(pk = order_item.order_product.pk)
    request.session['id'] = id
    request.session['order'] = order_item.order_product.pk
    context = {
        'stars' : {
            'total':rev.count(),
            'one': ((review.objects.filter(stars=1, product = id).count() / max(1, rev.count())) * 100),
            'two': ((review.objects.filter(stars=2, product = id).count() / max(1, rev.count())) * 100),
            'three': ((review.objects.filter(stars=3, product = id).count() / max(1, rev.count())) * 100),
            'four': ((review.objects.filter(stars=4, product = id).count() / max(1, rev.count())) * 100),
            'five': ((review.objects.filter(stars=5, product = id).count() / max(1, rev.count())) * 100),
        },
        'review': rev if rev else None,
        "pro": order_item.order_product,
        'per' : math.floor((100-((val.sale_price/val.max_price)*100))),

    }
    return render(request, 'user/review.html',context)


def add_review_view(request):
    if request.method =='POST':
        products = request.session.get('order')
        new= review.objects.create(
            customer = request.user,
            product = ProductVariant.objects.get(pk =products),
            stars = int(request.POST['stars']),
            review = str(request.POST['comment']),
        )
    return redirect('review:review_view',request.session.get('id') )
