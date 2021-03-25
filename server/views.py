from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import ServerDetailsForm
# Create your views here.
def server_index(request):
    form = ServerDetailsForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'title': 'Server Details',
        'server_details': form
    }
    return render(request, 'server/index.html', context)