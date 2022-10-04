import os
import random
import bs4
import wget
from django.shortcuts import render
import requests
from .models import Task
from django.http import HttpResponseRedirect, HttpResponseNotFound


def cat_parser():
    response = requests.get("https://yandex.ru/images/search?text=%D0%BA%D0%BE%D1%82%D1%8B%20%D1%81%D0%BC%D0%B5%D1%88"
                            "%D0%BD%D1%8B%D0%B5%20%D1%84%D0%BE%D1%82%D0%BE")
    soup = bs4.BeautifulSoup(response.text, "lxml")
    soup = soup.find_all('img', class_="serp-item__thumb justifier__thumb")
    number = random.randint(0, len(soup) - 1)
    img = str(soup[number])
    img = "https:" + img[img.find("//"):-3]
    return img


def index(request):
    tasks = Task.objects.all()
    return render(request, "index.html", {"tasks": tasks})



def create(request):
    if request.method == "POST":
        task = Task()
        task.name = request.POST.get("name")
        task.description = request.POST.get("description")
        task.cat_field = cat_parser()
        task.save()
    return HttpResponseRedirect("/")



def edit(request, id):
    try:
        task = Task.objects.get(id=id)

        if request.method == "POST":
            task.name = request.POST.get("name")
            task.description = request.POST.get("description")
            task.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"task": task})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")



def delete(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")
