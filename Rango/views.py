from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Rango.models import Category, Page
from Rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from bing_search import run_query


def index(request):
    context = {}

    category_list = Category.objects.order_by('-likes')[:5]
    context["categories"] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context["pages"] = page_list

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context['visits'] = visits

    return render(request, "Rango/index.html", context)


def category(request, category_name_slug):
    context = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        context['category_name'] = cat.name

        pages = Page.objects.filter(category=cat).order_by("-views")
        context["pages"] = pages

        context["category"] = cat

        context["category_name_slug"] = category_name_slug

    except Category.DoesNotExist:
        pass

    result_list = []
    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    context['result_list'] = result_list

    return render(request, "Rango/category.html", context)


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    return render(request, 'Rango/about.html', {'visits': count})


@login_required
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


@login_required
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

    return render(request, "Rango/add_page.html", context)


def track_url(request):
    url='/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url=page.url
            except:
                pass
    return HttpResponseRedirect(url)


@login_required
def like_category(request):
    cat_id = None
    likes = 0
    if request.method == "GET":
        cat_id = request.GET['category_id']
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)


def suggest_category(request):
    cat_list = []
    starts_with = ""
    if request.method == "GET":
        starts_with = request.GET['suggestion']

    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if len(cat_list) > 8:
        cat_list = cat_list[0:8]

    return render(request, "Rango/cats.html", {"cats":cat_list})


@login_required
def auto_add_page(request):
    context = {}
    if request.method == "GET":
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)

            pages = Page.objects.filter(category=category).order_by('-views')
            context["pages"] = pages
    return render(request, "Rango/page_list.html", context)

# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#             registered = True
#         else:
#             print user_form.errors, profile_form.errors
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
#     return render(request, "Rango/register.html", context)


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 return HttpResponse("Your Rango account is disabled")
#         else:
#             print "Invalid login details: {0} {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
#
#     context = {}
#     return render(request, "Rango/login.html", context)
#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/rango/')
