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
    return redirect(list_)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'todo/list.html', {'list': list_, 'error': error})
