from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'todo/home.html')


def view_list(request: HttpRequest) -> HttpResponse:
    items = Item.objects.all()
    return render(request, 'todo/list.html', {'items': items})


def new_list(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/todo/one-of-a-kind-list-in-the-world/')
