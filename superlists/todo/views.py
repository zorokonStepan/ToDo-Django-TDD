from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'todo/home.html')


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "todo/home.html", {"error": error})
    return redirect(f'/todo/{list_.id}/')


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    return render(request, "todo/list.html", {"list": _list})


def add_item(request, list_id):
    _list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=_list)
    return redirect(f"/todo/{_list.id}/")
