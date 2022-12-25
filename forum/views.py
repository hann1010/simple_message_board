#from _typeshed import Self
from django import db
from django.shortcuts import render
from .models import Forum_post
from .forms import FilterForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    #ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

def home(request):
    dic_x = {}
    filter_url_tmp = ''
    filter_url = ''
    filter_url_org = request.get_full_path()
    filter_url_org1 = '&' + (filter_url_org.replace('/', ''))
    if request.user.is_authenticated:
        filter_tmp = request.GET.get('title_filter')
        if filter_tmp != None:
            filter_str = filter_tmp
            filter_url_tmp = (filter_url_org1.replace('?', ''))
            position = filter_url_tmp.rfind('&')
            if position > 0:
                filter_url = filter_url_tmp[position:]
            else:
                filter_url = filter_url_tmp
        else:
            filter_str = ''
        filter_obj = FilterForm(request.GET or None)
        list_rows_tmp = request.user.profile.list_rows
        if list_rows_tmp > 0:
            list_rows_int = list_rows_tmp
        else:
            list_rows_int = 1
        if list_rows_tmp > 100:
            list_rows_int = 100
        db_data = Forum_post.objects.filter(title__icontains = filter_str).order_by('-date_posted')
        paginator = Paginator(db_data, list_rows_int)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        dic_x = {
            'title': 'home',
            'posts': page_data,
            'filter': filter_obj,
            'filter_url_str' : filter_url
        }
    return render(request, 'forum/index.html', dic_x)


@login_required
def latest_topics(request):
    items_in_page_tmp = request.user.profile.items_in_page
    if items_in_page_tmp > 0:
        items_in_page_int = items_in_page_tmp
    else:
        items_in_page_int = 1
    if items_in_page_tmp > 50:
        items_in_page_int = 50
    db_data = Forum_post.objects.filter(origin_post_id = 0).order_by('-date_posted')
    paginator = Paginator(db_data, items_in_page_int)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    dic_x = {
        'title': 'latest topics',
        'posts': page_data
    }
    return render(request, 'forum/itemview.html', dic_x)


@login_required
def latest_comments(request):
    items_in_page_tmp = request.user.profile.items_in_page
    if items_in_page_tmp > 0:
        items_in_page_int = items_in_page_tmp
    else:
        items_in_page_int = 1
    if items_in_page_tmp > 50:
        items_in_page_int = 50
    db_data = Forum_post.objects.exclude(origin_post_id = 0).order_by('-date_posted')
    paginator = Paginator(db_data, items_in_page_int)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    dic_x = {
        'title': 'latest comments',
        'posts': page_data
    }
    return render(request, 'forum/itemview.html', dic_x)


@login_required
def latest_all(request):
    items_in_page_tmp = request.user.profile.items_in_page
    if items_in_page_tmp > 0:
        items_in_page_int = items_in_page_tmp
    else:
        items_in_page_int = 1
    if items_in_page_tmp > 50:
        items_in_page_int = 50
    db_data = Forum_post.objects.all().order_by('-date_posted')
    paginator = Paginator(db_data, items_in_page_int)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    dic_x = {
        'title': 'latest all',
        'posts': page_data
    }
    return render(request, 'forum/itemview.html', dic_x)


class AllDetailView(LoginRequiredMixin, DetailView): #Show one post
    model = Forum_post
    template_name = 'forum/oneview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'one post'
        return context


class ThreadDetailView(LoginRequiredMixin, DetailView): #Show post thread
    model = Forum_post
    template_name = 'forum/itemview.html'

    def get_context_data(self, **kwargs):
        items_in_page_tmp = self.request.user.profile.items_in_page
        if items_in_page_tmp > 0:
            items_in_page_int = items_in_page_tmp
        else:
            items_in_page_int = 1
        if items_in_page_tmp > 50:
            items_in_page_int = 50
        context = super().get_context_data(**kwargs)
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        if db_data['origin_post_id'] == 0:
            post_id = db_data['id']
        else:
            post_id = db_data['origin_post_id']
        db_data = Forum_post.objects.filter(Q(id = post_id) | Q(origin_post_id = post_id)).order_by('date_posted')
        paginator = Paginator(db_data, items_in_page_int)
        page_number = self.request.GET.get('page')
        page_data = paginator.get_page(page_number)
        context["posts"] = page_data
        context["title"] = 'message thread'
        return context


class UserDetailView(LoginRequiredMixin, DetailView): #Show selected user information
    model = Forum_post
    template_name = 'forum/user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'User info'
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_topics')
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'new topic'
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/topic_new.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'Topic'
        messages.add_message(self.request, messages.INFO, 'Yours new topic has been saved!')
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_comments')
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_context"] = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        context["title"] = 'new comment' 
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/comment_new.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post_type = 'Comment'
        form.instance.title = 'Re: ' + db_data['title']
        if db_data['origin_post_id'] == 0:
            form.instance.origin_post_id = db_data['id']
        else:
            form.instance.origin_post_id = db_data['origin_post_id']
        info = 'Yours new comment to '+ db_data['title']+ ' has been saved!'
        messages.add_message(self.request, messages.INFO, info)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_all')
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'edit post'
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/edit_all.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        info = 'Post '+ db_data['title']+ ' has been updated!'
        messages.add_message(self.request, messages.INFO, info)
        return super().form_valid(form)

    def test_func(self):
        Forum_post = self.get_object()
        if self.request.user == Forum_post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'delete post'
        return context

    def test_func(self):
        Forum_post = self.get_object()
        if self.request.user == Forum_post.author and self.request.user.profile.user_level > 4:
            return True
        return False 