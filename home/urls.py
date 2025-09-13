from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('product/<slug:product_slug>/', views.ProductDetailsView.as_view(), name='product_details'),
    path('reply/<int:product_id>/<int:comment_id>/', views.PostAddReplyView.as_view(), name='add_reply'),
]
