from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm

from .form import CommentsForm
from .models import Post, Likes


class PostView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "blog/blog.html", {"post_list": posts})


class PostDetail(View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, "blog/blog_detail.html", {"post": post})


class AddComments(View):
    def post(self, request, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = pk
            form.save()

        return redirect(f"/{pk}")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(".")[0]
    else:
        print('>>>>>>>>>>>>>>>>>>else<<<<<<<<<<<<<<<<<<<<')
        ip = request.META.get('REMOTE_ADDR')
        print(ip)
    return ip


class AddLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            print("try")
            a = Likes.objects.get(ip=ip_client, post_id=pk)
            print(a)
            return redirect(f"/{pk}")
        except:
            print("except")
            new_like = Likes()
            new_like.ip = ip_client
            new_like.post_id = int(pk)
            new_like.save()
            return redirect(f"/{pk}")


@login_required
def profile_view(request):
    return render(request, 'profile/profile.html')


def logout_user(request):
    return redirect("/profile")


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
