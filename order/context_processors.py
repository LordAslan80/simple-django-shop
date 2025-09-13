from .cart import Cart


def cart_total_quantity(request):
    if request.user.is_authenticated and request.user.profile.active_order:
        return {'cart_total_quantity': len(Cart(request))}
    return {'cart_total_quantity': 0}