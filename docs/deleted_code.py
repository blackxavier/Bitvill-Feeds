# def delete_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     user_posts = False
#     if post.user == request.user:
#         post.delete()
#         redirect("home")
#     else:
#         user_posts = True
#         context = {"user_posts": user_posts}
#         return render(request, "feeds/index.html", context)
