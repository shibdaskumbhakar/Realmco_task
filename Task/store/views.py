from django.shortcuts import render, redirect, HttpResponse
from store.forms.authforms import UserCreationForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as userlogin
from store.models import Product, Cart
from django.views.generic import DetailView, DeleteView

from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


def home(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    cart = request.session.get('cart')
    print(cart)
    return render(request, template_name='store/home.html', context=context)


def login(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, template_name='store/login.html', context={
            'form': form
        })
    else:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                userlogin(request, user)
                cart = Cart.objects.filter(user=user)
                session_cart = []
                for c in cart:
                    obj = {
                        'item': c.product.id,
                        'quentity': c.quentity
                    }
                    session_cart.append(obj)
                request.session['cart'] = session_cart
                return redirect("home")

        else:
            return render(request, template_name='store/login.html', context={
                'form': form
            })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            return render(request, template_name='store/login.html')
        context = {
            "form": form
        }
        return render(request, template_name='store/signup.html', context=context)

    else:
        form = UserCreationForm()
        context = {
            "form": form
        }
    return render(request, template_name='store/signup.html', context=context)


def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    for c in cart:
        item_id = c.get('item')
        item = Product.objects.get(id=item_id)
        c['item'] = item
    print(cart)
    return render(request, template_name='store/cart.html', context={'cart': cart})


def logout(request):
    request.session.clear()
    return render(request, template_name='store/home.html')


class ProductDetailSlugViews(DetailView):

    queryset = Product.objects.all()
    template_name = "store/details.html"


def add_to_cart(request, slug):
    user = None
    item_id = None
    if request.user.is_authenticated:
        user = request.user
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    item = Product.objects.get(slug=slug)
    flag = True
    for cart_obj in cart:
        item_id = cart_obj.get('item')
        if item_id == item.id:
            flag = False
            cart_obj['quentity'] = cart_obj['quentity']+1
    if flag:
        cart_obj = {
            'item': item.id,
            'quentity': 1
        }
        cart.append(cart_obj)
    if user is not None:
        product_obj = Product.objects.get(slug=slug)
        existing = Cart.objects.filter(user=user, product=product_obj)
        if len(existing) > 0:
            obj = existing[0]
            obj.quentity = obj.quentity+1
            obj.save()
        else:
            c = Cart()
            c.user = user
            c.product = Product.objects.get(slug=slug)
            c.quentity = 1
            c.save()

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)


@staff_member_required
def admin(request):

    if request.method == "POST":
        slug = request.POST['slug']
        print(slug)
        product = Product.objects.get(slug=slug)
        product.delete()
        return render(request, template_name='store/admin.html')

    product = Product.objects.all()
    context = {
        "product": product
    }

    return render(request, template_name='store/admin.html', context=context)


