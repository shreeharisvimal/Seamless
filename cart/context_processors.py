from cart.models import Cart, Cart_Item
from user_side.models import Wishlist
from account.models import UserProfile

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

def profile_pic(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser :
            user = UserProfile.objects.get_or_create(user = request.user)
            user = UserProfile.objects.get(user = request.user)
            return {'my_pic': user.profile_pic }
        else:
            return {'my_pic': 0 }
    except Exception as e:
        print(f'the error is {e}')
        

        