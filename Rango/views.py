from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Rango.models import Category, Page
from Rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login


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

    context = {'form': form}
    return render(request, "Rango/add_category.html", context)


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

    context = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, "Rango/register.html", context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            print "Invalid login details: {0} {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")


    context = {}
    return render(request, "Rango/login.html", context)