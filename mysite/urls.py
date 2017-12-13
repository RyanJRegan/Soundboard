"""soundboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from soundboard import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login_or_signup/$', views.login_or_signup, name='login_or_signup'),
    url(r'^your_boards/$', views.your_boards, name='your_boards'),
    url(r'^boards/new/$', views.new_board, name='new_board'),
    url(r'^sounds/create/$', views.create_sound, name='crdeate_sound'),
    url(r'^soundboard/create/$', views.create_soundboard, name='create_soundboard'),
    url(r'^soundboard/(?P<id>[0-9]+)/$', views.create_soundboard, name='create_soundboard'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
