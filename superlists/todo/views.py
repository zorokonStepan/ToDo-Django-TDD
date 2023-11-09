from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'todo/home.html')


def new_list(request):
    _list = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=_list)
    return redirect(f"/todo/{_list.id}/")


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    return render(request, "todo/list.html", {"list": _list})


def add_item(request, list_id):
    _list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=_list)
    return redirect(f"/todo/{_list.id}/")
