import pprint

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post


# Create your views here.
def post_list(request):
    post_list_ = Post.published.all()  # 这个时候还没有访问数据库
    # Pagination with 3 posts per page
    paginator = Paginator(post_list_, 3)
    page_number = request.GET.get('page', 1)  # 如果没有page参数, 那么就取默认值1
    try:
        posts = paginator.page(page_number)
    # If page_number is less than 1, greater than max page number or not an integer
    except (PageNotAnInteger, EmptyPage):
        #  deliver the first page
        posts = paginator.page(1)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post_slug):
    # try:
    #     post = Post.published.get(id=id_)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post_slug)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
