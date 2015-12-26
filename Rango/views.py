from django.shortcuts import render
from django.http import HttpResponse
from Rango.models import Category, Page


def index(requests):
    context = {}

    category_list = Category.objects.order_by('-likes')[:5]
    context["categories"] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context["pages"] = page_list

    return render(requests, "Rango/index.html", context)


def category(requests, category_name_slug):
    context = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        context['category_name'] = cat.name

        pages = Page.objects.filter(category=cat)
        context["pages"] = pages

        context["category"] = cat

    except Category.DoesNotExist:
        pass

    return render(requests, "Rango/category.html", context)


def about(requests):
    html = "<p>This is the about page</p><a href='/rango'>Index</a>"
    return HttpResponse(html)
