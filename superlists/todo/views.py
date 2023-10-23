from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todo/')

    items = Item.objects.all()
    return render(request, 'todo/home.html', {'items': items})
