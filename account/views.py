from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserSignUpForm, UserSignInForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, logout, login
from order.models import Order


class DashboardView(LoginRequiredMixin, View):
    form_class_user = UpdateUserForm
    form_class_profile = UpdateProfileForm
    template_name = 'account/profile.html'
    
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self.user.is_staff:
            return redirect('/admin')
        form_user = self.form_class_user(instance=self.user)
        form_profile = self.form_class_profile(instance=self.user.profile)
        orders = Order.objects.filter(user=self.user, paid=True)
        return render(request, self.template_name, {'user':self.user, 'form_user':form_user, 'form_profile':form_profile, 'orders':orders})
    
    def post(self, request, *args, **kwargs):
        form_user = self.form_class_user(request.POST, request.FILES, instance=self.user)
        form_profile = self.form_class_profile(request.POST, request.FILES, instance=self.user.profile)
        if form_user.is_valid():
            form_user.save()
        if form_profile.is_valid():
            form_profile.save()
            return redirect('account:dashboard', self.user.id)
        return render(request, self.template_name, {'user':self.user, 'form_user':form_user, 'form_profile':form_profile})
    

class UserSignUpView(View):
    form_class = UserSignUpForm
    template_name = 'account/sign_up.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})
    

class UserSignInView(View):
    form_class = UserSignInForm
    template_name = 'account/sign_in.html'
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
        return render(request, self.template_name, {'form':form})


class UserSignOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')