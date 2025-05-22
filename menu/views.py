from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from menu.models import *
from tables.models import *
from menu.models import Menu
from tables.models import Table
from .models import FoodOrdered

# Create your views here.
def menu(request):
    dishes = Menu.objects.filter(is_available=True)
    
    context = {}  # Bạn có thể truyền dữ liệu sang template nếu cần
    return render(request, 'menu.html', {'new_dishes': dishes}) 


def add_to_cart(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        food_id = request.POST.get('food_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})

        if table_id not in cart:
            cart[table_id] = {}

        if food_id in cart[table_id]:
            cart[table_id][food_id] += quantity
        else:
            cart[table_id][food_id] = quantity

        request.session['cart'] = cart

        # Redirect về trang giỏ hàng của bàn đó
        return redirect('view_cart', table_id=table_id)

    return redirect('menu')



def view_cart(request, table_id):
    cart = request.session.get('cart', {})
    table_cart = cart.get(table_id, {})

    items = []
    total_quantity = 0
    for food_id, quantity in table_cart.items():
        try:
            food = Menu.objects.get(id=food_id)
            items.append({'food': food, 'quantity': quantity})
            total_quantity += quantity
        except Menu.DoesNotExist:
            pass

    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        return HttpResponse("Bàn không tồn tại", status=404)

    return render(request, 'cart.html', {
        'items': items,
        'total_quantity': total_quantity,
        'table': table,
    })


def remove_from_cart(request, table_id, food_id):
    cart = request.session.get('cart', {})
    if table_id in cart and food_id in cart[table_id]:
        del cart[table_id][food_id]
        request.session['cart'] = cart
    return redirect('view_cart', table_id=table_id)


def place_order(request, table_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        table_cart = cart.get(table_id, {})

        if not table_cart:
            return render(request, 'order_failed.html', {'reason': 'Giỏ hàng trống'})

        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return render(request, 'order_failed.html', {'reason': 'Bàn không tồn tại'})

        for food_id, quantity in table_cart.items():
            try:
                food = Menu.objects.get(id=food_id)
                if food.isOutOfStock:
                    return render(request, 'order_failed.html', {'reason': f'Món {food.name} hiện đã hết hàng'})
                FoodOrdered.objects.create(
                    food=food,
                    quantity=quantity,
                    table=table,
                    isServed=False
                )
            except Menu.DoesNotExist:
                continue

        # Xóa giỏ hàng bàn đó sau khi order
        del cart[table_id]
        request.session['cart'] = cart

        return render(request, 'order_success.html', {
            'table': table,
            'items': [(Menu.objects.get(id=fid), qty) for fid, qty in table_cart.items()]
        })

    return redirect('view_cart', table_id=table_id)

