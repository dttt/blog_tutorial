from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from blogengine.models import Post


class IndexView(generic.ListView):
    template_name = 'blogengine/post_list.html'

    def get_queryset(self):
        return Post.objects.all()


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blogengine/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter()
