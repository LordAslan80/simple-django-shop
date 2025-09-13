from django.urls import path
from . import views

app_name='account'
urlpatterns = [
    path('dashboard/<int:user_id>', views.DashboardView.as_view(), name='dashboard'),
    path('sign-up/', views.UserSignUpView.as_view(), name='sign_up'),
    path('sign-in/', views.UserSignInView.as_view(), name='sign_in'),
    path('sign-out/', views.UserSignOutView.as_view(), name='sign_out'),
]
