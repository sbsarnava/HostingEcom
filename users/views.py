from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from shop.models import Order, Cart
from .models import Profile
from .utils import render_to_pdf, verifyConnection
from django.views.generic import View
from django.core.paginator import Paginator
from .forms import ProfileAddressForm, verifyConnForm
import json


@login_required()
def profile(request):
    cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
    orders = Order.objects.filter(user=request.user, ordered=True)
    ordersNotDone = Order.objects.filter(user=request.user, ordered=False)
    userProfile = Profile.objects.filter(user=request.user)[0]
    # Paginator for Orders Completed or for Invoice
    orderPaginator = Paginator(orders, 5)
    orderPage = request.GET.get('page1')
    orders_done = orderPaginator.get_page(orderPage)
    # Paginator for Uncompleted Orders
    orderNotDonePaginator = Paginator(ordersNotDone, 5)
    orderNotDonePage = request.GET.get('page2')
    orders_not_done = orderNotDonePaginator.get_page(orderNotDonePage)
    context = {
        'userProfile': userProfile,
        'ordersNotDone': orders_not_done,
        'orders': orders_done,
        'cart': cart
    }
    return render(request, 'accounts/profile.html', context)


@login_required()
def profile_orders(request):
    cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
    orders = Order.objects.filter(user=request.user, ordered=True)

    context = {
        'orders': orders,
        'cart': cart
    }
    return render(request, 'accounts/profile_orders.html', context)


@login_required()
def profile_products(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
    context = {
        'cart': cart,
        'orders': orders
    }
    return render(request, 'accounts/profile_products.html', context)


@login_required()
def invoicelist(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
    context = {
        'orders': orders,
        'cart': cart
    }
    return render(request, 'accounts/profile_invoiceslist.html', context)


class GenerateInvoice(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(orderId=self.kwargs['oid'])
        context = {
            'order': order
        }
        pdf = render_to_pdf('pdf/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


@login_required()
def profile_settings(request):
    cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
    profile = Profile.objects.get(user=request.user)
    profileform = ProfileAddressForm(initial={
        'fullname': profile.fullname,
        'address1': profile.address1,
        'address2': profile.address2,
        'pincode': profile.pincode,
        'state': profile.state,
        'country': profile.country,
        'phonenumber': profile.phonenumber,
    })

    if request.method == 'POST':
        profileform = ProfileAddressForm(request.POST)
        if profileform.is_valid():
            profile.fullname = profileform.cleaned_data['fullname']
            profile.address1 = profileform.cleaned_data['address1']
            profile.address2 = profileform.cleaned_data['address2']
            profile.pincode = profileform.cleaned_data['pincode']
            profile.state = profileform.cleaned_data['state']
            profile.country = profileform.cleaned_data['country']
            profile.phonenumber = profileform.cleaned_data['phonenumber']
            profile.save()

    context = {
        'cart': cart,
        'form': profileform
    }
    return render(request, 'accounts/profile_settings.html', context)


@login_required()
def changeAPISettings(request):
    if request.user.groups.filter(name='admin').exists() or request.user.is_superuser:
        cart = Cart.objects.filter(user=request.user).order_by('-id')[0]
        conn = False
        ver = verifyConnForm()
        if request.method == 'POST' and 'check' in request.POST:
            content = json.loads(verifyConnection().content)
            if content['verifyConn'] == 1:
                conn = True
            else:
                conn = False

        context = {
            'form': ver,
            'cart': cart,
            'result': conn
        }
        return render(request, 'accounts/apisettings.html', context)
    else :
        return HttpResponseForbidden()