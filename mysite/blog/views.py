import pprint

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post, Comment
from .forms import ShareWithEmailPostForm, CommentForm


# Create your views here.
def post_list(request, tag_slug=None):
    post_list_ = Post.published.all()  # 这个时候还没有访问数据库
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # post(blog_post)和tag(taggit_tag)是 Many-to-many relationship, 关系表是taggit_taggeditem.
        post_list_ = post_list_.filter(tags__in=[tag])  # 这个时候仍然没有访问数据库
    # Pagination with 3 posts per page
    paginator = Paginator(post_list_, 3)
    page_number = request.GET.get('page', 1)  # 如果没有page参数, 那么就取默认值1
    try:
        posts = paginator.page(page_number)
    # If page_number is less than 1, greater than max page number or not an integer
    except (PageNotAnInteger, EmptyPage):
        #  deliver the first page
        posts = paginator.page(1)  # 这个时候仍然没有访问数据库
    # Remember that QuerySets are lazy. The QuerySets to retrieve posts will only be evaluated when you
    # loop over the post list when rendering the template.
    return render(request,
                  'blog/post/list.html',
                  {
                      'posts': posts,
                      'tag': tag
                  })


# # The PostListView view is analogous to the post_list view we built previously. We have implemented
# # a class-based view that inherits from the ListView class. We have defined a view with the following
# # attributes:
# # • We use queryset to use a custom QuerySet instead of retrieving all objects. Instead of defining
# # a queryset attribute, we could have specified model = Post and Django would have built the
# # generic Post.objects.all() QuerySet for us.
# # • We use the context variable posts for the query results. The default variable is object_list
# # if you don’t specify any context_object_name.
# # • We define the pagination of results with paginate_by, returning three objects per page.
# # • We use a custom template to render the page with template_name. If you don’t set a default
# # template, ListView will use blog/post_list.html by default.
# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


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
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'form': form
                  })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = ShareWithEmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            # If your form data does not validate, cleaned_data will contain only the valid fields.
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, "704379675@qq.com", [cd['to']])
            sent = True
    else:
        form = ShareWithEmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent
                  })


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment: Comment = None
    # A comment was posted
    form: CommentForm = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        # The save() method is available for ModelForm but not for Form instances since
        # they are not linked to any model.
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request,
                  'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })
