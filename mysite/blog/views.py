from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, FormView
from django.core.mail import send_mail
from blog.forms import EmailPostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


class PostListByTagview(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.published.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tag"] = self.tag
        return data


class PostShareView(SuccessMessageMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "mail sent"

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(
            Post, id=self.kwargs.get("post_id")
        )
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(PostShareView, self).form_valid(form)

    def send_mail(self, valid_data):
        post_url = self.request.build_absolute_uri(
            self.post_object.get_absolute_url()
        )
        send_mail(
            message=f"Read {self.post_object.title} at { post_url }\n\n"
            f"{valid_data['from_name']}'s message: {valid_data['share_message']}",
            from_email=valid_data["from_email"],
            subject=f"{valid_data['from_name']} recommends you read {self.post_object.title}",
            recipient_list=[valid_data["to_email"]],
        )
