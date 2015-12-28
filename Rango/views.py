from django.shortcuts import render
from django.http import HttpResponse
from Rango.models import Category, Page
from Rango.forms import CategoryForm, PageForm


def index(request):
    context = {}

    category_list = Category.objects.order_by('-likes')[:5]
    context["categories"] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context["pages"] = page_list

    return render(request, "Rango/index.html", context)


def category(request, category_name_slug):
    context = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        context['category_name'] = cat.name

        pages = Page.objects.filter(category=cat)
        context["pages"] = pages

        context["category"] = cat

        context["category_name_slug"] = category_name_slug

    except Category.DoesNotExist:
        pass

    return render(request, "Rango/category.html", context)


def about(request):
    html = "<p>This is the about page</p><a href='/rango'>Index</a>"
    return HttpResponse(html)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, "Rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

