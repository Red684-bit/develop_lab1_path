from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

def index(request):
    return HttpResponse("Главная страница сайта")

def books(request, id):
    dict = {1: "Анна Каренина", 2: "Мастер и Маргарита", 3: "Преступление и наказание"}
    if id in dict:
        return HttpResponse(f"Книга {dict[id]}")
    else:
        return HttpResponseNotFound("Книги нет")
    
def search(request):
    q = request.GET.get('q')
    type = request.GET.get('type')
    return HttpResponse(f"Вы ищете: '{q}'. Тип поиска: '{type}'.")

def set_theme(request):
    color = request.GET.get('color')
    response = HttpResponseRedirect("/theme")
    response.set_cookie('site_theme', color, max_age=60*60*24*30)
    return response

def theme(request):
    color = request.COOKIES.get("site_theme")
    if color:
        return HttpResponse(f"Текущая тема: {color}")
    else:
        return HttpResponse("Тема не установлена")
    
def dop(request, id, rev):
    return HttpResponse(f"Отзыв #{id} к книге '{rev}'")

