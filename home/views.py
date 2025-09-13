from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Category, Comment
from order.forms import AddToCardForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CommentCreateForm, CommentReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category_filter = Category.objects.get(slug=category_slug)
            if not category_filter.is_sub:
                sub_categories = category_filter.scategory.all()
                if sub_categories.exists():
                    products = products.filter(category__in=sub_categories)
                else:
                    products = products.filter(category=category_filter)            
            else:
                products = products.filter(category=category_filter)
        return render(request, 'home/products.html', {'products':products, 'categories':categories})


class ProductDetailsView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    
    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['product_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, product_slug):
        comments = self.product.pcomments.filter(is_reply=False)
        form = AddToCardForm()
        return render(request, 'home/product_details.html', {'product':self.product, 'form':form, 'comments':comments,
                                                             'comment_form':self.form_class, 'comment_reply_form':self.form_class_reply})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product
            new_comment.save()
            return redirect('home:product_details', self.product.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    
    def post(self, request, product_id, comment_id):
        product = get_object_or_404(Product, id=product_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()
        return redirect('home:product_details', product.slug)