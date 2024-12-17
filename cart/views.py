# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart/cart.html', {'cart': cart, 'items': items, 'total': total})

@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
    
    messages.success(request, f'تمت إضافة {product.name} إلى عربة التسوق.')
    
    # حساب عدد العناصر في العربة
    cart_count = sum(item.quantity for item in cart.items.all())
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_count,
            'message': f'تمت إضافة {product.name} إلى عربة التسوق.'
        })
    
    return redirect('cart')

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'تمت إزالة العنصر من عربة التسوق.')
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_count = sum(item.quantity for item in cart.items.all())
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_count,
            'new_total': total
        })
    
    return redirect('cart')

@require_POST
@login_required
def proceed_to_payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in items)
    
    # هنا يمكنك إضافة منطق الدفع الخاص بك
    
    cart.items.all().delete()
    messages.success(request, 'تم إتمام عملية الدفع بنجاح!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'تم إتمام عملية الدفع بنجاح!'})
    
    return redirect('index')
