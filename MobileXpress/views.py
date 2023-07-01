from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from MobileXpress.forms import BootstrapAuthenticationForm, RegistrationForm, OrderForm, PaymentForm, PhoneForm, \
    PhoneColorQuantityFormSet
from MobileXpress.models import *


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            cart = ShoppingCart.objects.filter(
                user=CustomUser.objects.all().filter(user=form.get_user()).first()).first()
            if not cart:
                new_cart = ShoppingCart(user=CustomUser.objects.all().filter(user=form.get_user()).first())
                new_cart.save()
            return redirect('/')
    return render(request, 'login.html', {'form': BootstrapAuthenticationForm()})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request, 'register.html', {'form': RegistrationForm()})


def store(request):
    return render(request, 'store.html', context={
        "phones": Phone.objects.all()
    })


def details(request, pk):
    has_in_stock = False
    colors = PhoneColorQuantity.objects.all().filter(phone__pk=pk)
    for pcq in colors:
        if pcq.quantity > 0:
            has_in_stock = True
    phone = get_object_or_404(Phone, pk=pk)
    if request.user.is_authenticated:
        already_in_cart = len(
            CartItem.objects.all().filter(cart=get_shopping_cart_for_logged_user(request), phone=phone)) > 0
    else:
        already_in_cart = False
    return render(request, 'details.html', context={
        "phone": phone,
        "colors": colors,
        "has_in_stock": has_in_stock,
        "successfully_added_to_cart": None,
        "already_in_cart": already_in_cart
    })


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def add_to_cart(request, pk):
    has_in_stock = False
    colors = PhoneColorQuantity.objects.all().filter(phone__pk=pk)
    for pcq in colors:
        if pcq.quantity > 0:
            has_in_stock = True
    if request.method == "POST":
        phone = get_object_or_404(Phone, pk=pk)
        quantity = int(request.POST.get("quantity"))
        color_id = request.POST.get("color")
        color = get_object_or_404(Color, pk=color_id)
        pcq = PhoneColorQuantity.objects.all().filter(phone=phone, color=color_id).first()
        if pcq.quantity > quantity:
            cart_item = CartItem(phone=phone, quantity=quantity, color=color,
                                 cart=get_shopping_cart_for_logged_user(request))
            cart_item.save()
        return render(request, 'details.html', context={
            "phone": phone,
            "colors": colors,
            "has_in_stock": has_in_stock,
            "successfully_added_to_cart": pcq.quantity > quantity,
            "already_in_cart": None
        })


def get_shopping_cart_for_logged_user(request):
    return ShoppingCart.objects.all().filter(user=CustomUser.objects.all().filter(user=request.user).first()).first()


def shopping_cart(request):
    total_amount = 0
    shoppingCart = get_shopping_cart_for_logged_user(request)
    cart_items = CartItem.objects.all().filter(cart=shoppingCart)
    for cart_item in cart_items:
        total_amount += cart_item.subtotal()
    return render(request, "shopping_cart.html", {
        "shopping_cart": shoppingCart,
        "cart_items": cart_items,
        "total_amount": total_amount
    })


def order_form(request):
    if request.method == "POST":
        print("Here")
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = CustomUser.objects.all().filter(user=request.user).first()
            shoppingCart = get_shopping_cart_for_logged_user(request)
            order.cart = shoppingCart
            order.order_status = "Created"
            total_amount = 0
            for cart_item in CartItem.objects.all().filter(cart=get_shopping_cart_for_logged_user(request)):
                phone = cart_item.phone
                color = cart_item.color
                pcq = PhoneColorQuantity.objects.all().filter(phone=phone, color=color).first()
                pcq.quantity -= cart_item.quantity
                pcq.save()
                total_amount += cart_item.subtotal()

            order.total_amount = total_amount

            shoppingCart.user = None
            shoppingCart.save()
            cart = ShoppingCart(user=CustomUser.objects.all().filter(user=request.user).first())
            cart.save()
            order.save()
            if order.payment_method == "Card":
                return redirect('/payment_form/' + str(order.id))
            else:
                return redirect('/successful_order')
    return render(request, "order_form.html", context={
        "form": OrderForm()
    })


def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "order_details.html", context={
        "order": order,
        "cart_items": CartItem.objects.all().filter(cart=order.cart)
    })


def my_orders(request):
    return render(request, "my_orders.html", context={
        "orders": Order.objects.all().filter(user__user=request.user)
    })


def admin_orders(request):
    return render(request, "admin_orders.html", context={
        "created_orders": Order.objects.all().filter(order_status="Created"),
        "in_delivery_orders": Order.objects.all().filter(order_status="InDelivery"),
        "finished_orders": Order.objects.all().filter(order_status="Finished")
    })


def payment_form(request, pk):
    if request.method == "POST":
        order = get_object_or_404(Order, pk=pk)
        form = PaymentForm(request.POST)
        payment = form.save(commit=False)
        payment.order = order
        payment.save()
        return redirect("/successful_order")
    return render(request, "payment_form.html", context={
        "form": PaymentForm()
    })


def successful_order(request):
    return render(request, "successful_order.html")


def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    for cart_item in CartItem.objects.all().filter(cart=order.cart):
        phone = cart_item.phone
        color = cart_item.color
        pcq = PhoneColorQuantity.objects.all().filter(phone=phone, color=color).first()
        pcq.quantity += cart_item.quantity
        pcq.save()
    order.delete()
    return redirect('my_orders')


def finished_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.order_status = 'Finished'
    order.save()
    return redirect('my_orders')


def in_delivery_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.order_status = 'InDelivery'
    order.save()
    return redirect('admin_orders')


def profile(request):
    return render(request, "profile.html", context={
        "current_user": CustomUser.objects.all().filter(user=request.user).first()
    })


def about_us(request):
    return render(request, "about_us.html")


def add_product(request):
    form = PhoneForm()
    formset = PhoneColorQuantityFormSet(queryset=PhoneColorQuantity.objects.none())

    if request.method == 'POST':
        form = PhoneForm(request.POST, request.FILES)
        formset = PhoneColorQuantityFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            phone = form.save()
            formset.instance = phone
            formset.save()
            return redirect('store')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'add_product.html', context)


def delete_product(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    if request.method == "POST":
        phone.delete()
        return redirect('successful_delete_product')
    return render(request, "delete_product.html", context={
        "phone": phone
    })


def successful_delete_product(request):
    return render(request, "successful_delete_product.html")


def delete_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('shopping_cart')