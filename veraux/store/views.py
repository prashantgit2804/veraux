from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category, Wishlist, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Merge session cart if exists? skipping for now
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def shop(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'product.html', {'product': product, 'related_products': related_products})

def cart(request):
    cart_obj = get_cart(request)
    return render(request, 'cart.html', {'cart': cart_obj})

def checkout(request):
    cart_obj = get_cart(request)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        
        # Calculate total
        total_amount = cart_obj.total_price
        
        # Create Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            country=country,
            zip_code=zip_code,
            total_amount=total_amount
        )
        
        # Create OrderItems
        for item in cart_obj.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            
        # Clear Cart
        cart_obj.items.all().delete()
        cart_obj.delete()
        
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('home')
        
    return render(request, 'checkout.html', {'cart': cart_obj})

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')
            
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')
            
        # Create user
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def wishlist(request):
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# AJAX Views

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_obj = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return JsonResponse({
        'status': 'success', 
        'cart_count': cart_obj.items.count(), 
        'total_price': float(cart_obj.total_price),
        'message': f'{product.name} added to cart'
    })

def update_cart(request, item_id):
    cart_obj = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart_obj)
    
    # Get action (increment/decrement) or quantity from POST request
    try:
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
        
        if cart_item.quantity < 1:
            cart_item.delete()
        else:
            cart_item.save()
            
        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity,
            'item_total': float(cart_item.total_price),
            'cart_total': float(cart_obj.total_price),
            'cart_count': cart_obj.items.count()
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def remove_from_cart(request, item_id):
    cart_obj = get_cart(request)
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart_obj)
        cart_item.delete()
        return JsonResponse({
            'status': 'success',
            'cart_total': float(cart_obj.total_price),
            'cart_count': cart_obj.items.count(),
            'message': 'Item removed from cart'
        })
    except Exception as e:
         return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def cart_data(request):
    cart_obj = get_cart(request)
    items = []
    for item in cart_obj.items.all():
        items.append({
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image': item.product.image.url if item.product.image else '',
            'id': item.id,
            'total': float(item.total_price)
        })
    return JsonResponse({'items': items, 'total': float(cart_obj.total_price), 'count': cart_obj.items.count()})

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Please login to add to wishlist'}, status=401)
    
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({'status': 'success', 'message': 'Added to wishlist'})

def remove_from_wishlist(request, product_id):
    if not request.user.is_authenticated:
         return JsonResponse({'status': 'error', 'message': 'Login required'}, status=401)
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return JsonResponse({'status': 'success', 'message': 'Removed from wishlist'})
