from django.urls import path
from django.urls import re_path

from . import views
from .views import serve_threejs_content

urlpatterns = [
    path("threejs_content/", serve_threejs_content, name="threejs_content"),
    # re_path(
    #     r"^(?P<year>\d{4})-(?P<pk>\d+)/$",
    #     views.XRPrioDetailView.as_view(),
    #     name="topic-detail",
    # ),
    # re_path(
    #     r"^(?P<slug>[-\w_]+)/$", views.XRPrioDetailView.as_view(), name="topic-redirect"
    # ),
]
