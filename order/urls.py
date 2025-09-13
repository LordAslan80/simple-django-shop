from django.urls import path
from . import views


app_name='order'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order_detail/<int:order_id>', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/add/<int:product_id>', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>', views.CartRemoveView.as_view(), name='cart_remove'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('product-plus/<int:product_id>', views.CartProductPlusView.as_view(), name='product_plus'),
    path('product-minus/<int:product_id>', views.CartProductMinusView.as_view(), name='product_minus'),
    path('delivery-apply/<int:delivery_id>', views.DeliveryApplyView.as_view(), name='apply_delivery'),
    path('coupon-apply/', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
