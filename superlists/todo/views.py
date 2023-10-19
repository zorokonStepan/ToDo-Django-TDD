from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()
    return render(request, 'todo/home.html', {'new_item_text': item.text})
