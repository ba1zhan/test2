"""
URL configuration for got project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import path

from series.views import (
    SeriesCreateView,
    SeriesListView,
    base,
    delete_series,
    series_create,
    series_detail,
    series_list,
)
from user.views import login_user, logout_user, profile, register, update_profile

class_urls = [
    path("class/series/", SeriesListView.as_view()),
    path("class/series_create/", SeriesCreateView.as_view()),
]

users = [
    path("register/", register),
    path("login/", login_user),
    path("logout/", logout_user),
    path("profile/", profile),
    path("update_profile/", update_profile),
    
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base),
    path("series/", series_list),
    path("series/<int:series_id>/", series_detail),
    path("series_create/", series_create),
    path("series_delete/<int:series_id>/", delete_series),
    *users,
    *class_urls
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)