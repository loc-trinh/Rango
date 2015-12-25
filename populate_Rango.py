import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webProject.settings')
django.setup()

from Rango.models import Category, Page


def populate():
    python_category = add_category("Python", views=128, likes=64)
    add_page(category=python_category,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/")
    add_page(category=python_category,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")
    add_page(category=python_category,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/")

    django_category = add_category("Django", views=64, likes=32)
    add_page(category=django_category,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")
    add_page(category=django_category,
             title="Django Rocks",
             url="http://www.djangorocks.com/")
    add_page(category=django_category,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/")

    frame_category = add_category("Other Frameworks", views=32, likes=16)
    add_page(category=frame_category,
             title="Bottle",
             url="http://bottlepy.org/docs/dev/")
    add_page(category=frame_category,
             title="Flask",
             url="http://flask.pocoo.org")

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_page(category, title, url, views=0):
    page = Page.objects.get_or_create(category=category, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page


def add_category(name, views, likes):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()

