from django.shortcuts import redirect, render,get_object_or_404
from .models import Product, Category, Customer, Order, OrderItem, Cart, CartItem, Review
from .forms import ProductForm,UserRegistrationForm
from django.contrib import messages
from django.db.models import Avg


from .forms import ProductForm,UserRegistrationForm,CustomerForm,ReviewForm

#CategoryForm, CustomerForm, OrderForm, OrderItemForm, CartForm, CartItemForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    return render(request, 'index.html')

# ------------- PRODUCT -------------
def product_list(request):
    print("PRODUCT LIST VIEW CALLED")
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_list.html', {'products': products}) 


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
    })


def category_product_list(request, category):
    products = Product.objects.filter(category_id=category).order_by('-created_at')
    return render(request, 'categorized.html', {'products': products, 'category': category})
  
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart')

@require_POST
def update_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        action = request.POST.get("action")
        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect("cart")


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def place_order(request):
    # Fetch cart items if you want to display them
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'place_order.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
@require_POST
def confirm_order(request):
    payment_method = request.POST.get("payment_method")
    
    # Here you would normally save the order to the database
    # For now we just clear the cart
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    
    messages.success(request, f"Order placed successfully with {payment_method.upper()}!")
    return redirect('product_list')



@login_required
# To add product into the website from the seller side
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
        
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
#To edit the product
def edit_product(request,id):
    product=get_object_or_404(Product,pk=id,user=request.user )
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')

    else:
        form=ProductForm(instance=product)
        return render(request, 'add_product.html', {'form': form})
    
@login_required
    #To delete the product
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

#User Registration
def register(request):
    if request.method=='POST':
        form =UserRegistrationForm(request.POST)
    
        if form.is_valid():
            user=form.save(commit=False)    
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
    

    else:
        form =UserRegistrationForm()
        

    return render(request, 'registration/register.html', {'form': form})


#To search the product
def search_product(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'search.html', {'query': query, 'products': products})


# ------------- CATEGORY -------------
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

#--------------REVIEW -------------

@login_required
def review_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('product_detail', id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'review_add.html', {'form': form ,'product': product})

def report(request):
    return render(request, 'report.html')