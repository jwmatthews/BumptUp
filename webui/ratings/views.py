from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader

from ratings.models import Category, Rating

#index
def index(request):
    # Allow a user to edit their own categories
    # Allow a user to vote on other peoples categories (maybe restrict to organization)
    categories = Category.objects.all().order_by('title')
    return render_to_response('ratings/index.html', {"categories":categories})

#details
def detail(request, category_id):
    try:
        c = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    return render_to_response("ratings/detail.html", {"category": c})

#rate
def rate(request, category_id):
    return HttpResponse("Rate holder for categories: %s" % (category_id))


