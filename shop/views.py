import datetime
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import BillingForm
from users.utils import randomNumber


def index(request):
    plans = Item.objects.all()

    if request.user.is_authenticated:
        cart1 = Cart.objects.filter(user=request.user).order_by('-id')[0]
        context = {
            'title': 'GitDev - Get Your Business online',
            'plans': plans,
            'cart': cart1
        }
    else:
        context = {
            'title': 'GitDev - Get Your Business online',
            'plans': plans,
        }
    return render(request, 'shop/index.html', context)


def store(request):
    context = {
        'title': 'GitDev - Products',
    }
    return render(request, 'shop/store.html', context)


@login_required
def cart(request):
    plans = Item.objects.all()
    context = {
        'plan': plans
    }
    return render(request, 'shop/cart.html', context)


@login_required
def checkout(request):
    if request.method == 'GET':
        billingaddress = BillingAddress.objects.filter(saveAddress=True)
        cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
        total = 0
        country = Country.objects.all()
        form = BillingForm()
        for x in cart.item.all():
            total += x.quantity * x.item.price
        context = {
            'title': 'GitDev - Checkout',
            'cart': cart,
            'total': total,
            'country': country,
            'form': form,
            'billing': billingaddress
        }
        return render(request, 'shop/checkout.html', context)
    # Used this method so that I can better control the flow
    elif request.method == 'POST':
        form = BillingForm(request.POST or None)
        if form.is_valid():
            billing = BillingAddress.objects.create(user=request.user, firstname=form.cleaned_data['firstname'],
                                                    lastname=form.cleaned_data['lastname'],
                                                    phonenumber=form.cleaned_data['phonenumber'],
                                                    email=form.cleaned_data['email'],
                                                    address1=form.cleaned_data['address1'],
                                                    address2=form.cleaned_data['address2'],
                                                    city=form.cleaned_data['city'],
                                                    country=form.cleaned_data['country'],
                                                    state=form.cleaned_data['state'],
                                                    pincode=form.cleaned_data['pincode'],
                                                    saveAddress=form.cleaned_data['saveAddress'])
            order = Order.objects.create(user=request.user,
                                         cartItems=Cart.objects.filter(user=request.user).order_by('-id')[0],
                                         billingAddress=billing)

            if form.cleaned_data['payment'] == 'cash':
                # Wrap this code to a roll off mode
                with transaction.atomic():
                    order.ordered = True
                    order.placed_date = datetime.now()
                    # Fix this part so that the order items in the current Cart is ordered to True
                    orderItems = OrderItem.objects.filter(user=request.user, ordered=False)

                    for items in orderItems:
                        items.ordered = True
                        items.save()
                    billing.save()
                    order.save()
                    Cart.objects.create(user=request.user)
                    return redirect('shop:cash-payment')
            elif form.cleaned_data['payment'] == 'razorpay':
                # Enter code for RazorPay Payment
                return redirect('shop:razor-payment')

            return HttpResponse('Order Failed')

        return HttpResponse(form.errors)


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        cart2 = Cart.objects.filter(user=request.user).order_by('-id')[0]
        orderItem, createdOrderItem = OrderItem.objects.get_or_create(user=request.user,
                                                                      item=Item.objects.get(id=request.POST['pk']),
                                                                      ordered=False)
        if createdOrderItem:
            cart2.item.add(orderItem)
        else:
            orderItem.quantity = orderItem.quantity + 1
            orderItem.save()
    return HttpResponse('')


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        orderItem = OrderItem.objects.get(user=request.user,
                                          item=Item.objects.get(id=request.POST['pk']), ordered=False)
        orderItem.quantity = orderItem.quantity - 1
        orderItem.save()
    return HttpResponse('')


@login_required
def cash_payment(request):
    return HttpResponse("You have selected cash payment")


@login_required
def razorpay_payment(request):
    return HttpResponse("You have selected razorpay payment")


def getAddress(request):
    if request.is_ajax():
        billing = BillingAddress.objects.get(id=request.GET['pk'])
        if request.user == billing.user:
            data = {
                'firstname': billing.firstname,
                'lastname': billing.lastname,
                'address1': billing.address1,
                'address2': billing.address2,
                'email1': billing.email,
                'phonenumber': billing.phonenumber,
                'state': billing.state,
                'city': billing.city,
                'pincode': billing.pincode,
                'country': billing.country
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('Failed')
