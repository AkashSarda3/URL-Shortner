"""url_shortner_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from shortner.views import NewView, StubView, UpdateView, DeleteView, delete_all_urls
from shortner.views import CustomView, home, signin, signout, signup, about_us, create_url
from shortner.views import login_test, ListUrlsView, homepage, StatsView

urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    # homepage/new to get it as post message in homepage. Figure it out later.
    path('new', NewView.as_view(), name='add_new'),
    path("delete/<slug:special_code>", DeleteView.as_view(), name='delete'),
    path('delete_all/', delete_all_urls, name='delete_all_urls'),
    path("stub/<slug:stub>/", StubView.as_view(), name='stub'),
    path("update/", UpdateView.as_view(), name='update'),
    path("custom/", CustomView.as_view(), name='custom'),
    path('', home, name="home"),
    path("test/", login_test, name="Test"),
    path('list', ListUrlsView.as_view(), name="list"),
    path('stats/', StatsView.as_view(), name='stats'),
    path('stats/export-csv/', StatsView.as_view(), name='export_csv'),
    path('signup', signup, name="signup"),
    path('signin', signin, name="signin"),
    path('signout', signout, name="signout"),
    path('about-us/', about_us, name='about_us'),
    path('index/', create_url, name = 'index'),
    # re_path(r'homepage/(?P<fname>[\w-]+)/$', homepage, name='homepage' ),
    path('homepage/<str:fname>', homepage, name='homepage')
]
