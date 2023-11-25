from cart.models import Cart, Cart_Item
from user_side.models import Wishlist

def count_wish(request):
    try:
        return {'wish_count': Wishlist.objects.filter(my_user = request.user).count()}
    except:
        return {'wish_count': 0}

def count_cart(request):
    cart_count = 0
    try:
        cart = Cart.objects.get(user = request.user)
        if cart:
            cart_count = Cart_Item.objects.filter(cart =cart).count()
        else:
            cart_count = 0
    except:
        pass
    return {'cart_count': cart_count}