from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from feeds.forms import PostForm
from feeds.models import Post, Report
from django.db.models import Count
from datetime import datetime

# HOME PAGE VIEW
def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
        posts = Post.objects.filter(hidden=False).order_by("-date_posted").all()
    context = {"form": form, "posts": posts}
    return render(request, "feeds/index.html", context)


# MODERATOR REPORT VIEW
@permission_required("feeds.view_report", raise_exception=True)
def report(request):
    reports = (
        Post.objects.annotate(times_reported=Count("report"))
        .filter(times_reported__gt=0)
        .all()
    )
    context = {"reports": reports}
    return render(request, "feeds/reports.html", context)


# REPORT A POST VIEW
def user_reports_post(request, post_id):
    post = Post.objects.get(id=post_id)
    report, created = Report.objects.get_or_create(reported_by=request.user, post=post)
    if created:
        report.save()
    return redirect("home")


# DELETE A POST VIEW
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user_posts = False
    if post.user == request.user:
        post.delete()
    return redirect("home")


# MODERATOR HIDE A POST VIEW
@permission_required("feedapp.change_post", raise_exception=True)
def hide_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.hidden = True
    post.date_hidden = datetime.now()
    post.hidden_by = request.user
    post.save()
    return redirect("reports")


# MODERATOR BLOCK A POST VIEW
@permission_required("feedapp.change_user")
def block_user(request, user_id):
    User = get_user_model()

    user = User.objects.get(id=user_id)
    for post in user.post_set.all():
        if not post.hidden:
            post.hidden = True
            post.hidden_by = request.user
            post.date_hidden = datetime.now()
            post.save()

    user.is_active = False
    user.save()

    return redirect("reports")


# MODERATOR LOGOUT VIEW
@login_required
def logout_user_out(request):
    logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = "http://127.0.0.1:8000"  # this can be current domain
    return redirect(
        f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"
    )
