from unicodedata import name
from django.urls import path
from feeds.views import (
    report,
    index,
    hide_post,
    block_user,
    logout_user_out,
    delete_post,
    user_reports_post,
)


urlpatterns = [
    path("", index, name="home"),
    path("reports/", report, name="reports"),
    path("logout/", logout_user_out, name="logout_user"),
    path("delete/<int:post_id>/", delete_post, name="delete_post"),
    path("report_post/<int:post_id>/", user_reports_post, name="user_report_post"),
    path("hide_post/<post_id>/", hide_post, name="hide_post"),
    path("block_user/<user_id>/", block_user, name="block_user"),
]
