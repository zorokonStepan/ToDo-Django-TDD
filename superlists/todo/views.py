from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'todo/home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })

    # if request.method == "POST":
    #     return HttpResponse(request.POST['item_text'])
    # return render(request, 'todo/home.html')
