from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone

from .models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/home.html', {'products': products})

@login_required
def create(request):
    if request.method == "POST":
        
        # TODO Can these be required fields = TRUE in models???
        if request.POST['title'] and request.POST['url'] and request.POST['body'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']

            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
                
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'message':'All fields must be completed'})
    
    return render(request, 'products/create.html')


def detail(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product':product
    }
    return render(request, 'products/detail.html', context)

@login_required
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
                
        return redirect('/products/' + str(product.id))
