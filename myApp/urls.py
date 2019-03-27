"""myApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

#Always use include when including other URL patterns except for admin.size.urls
#The idea is to make it easy to plug and play URLs, especially since polls have their own URLconfs (polls/urls.py)
from django.contrib import admin
from django.urls import include, path

#Wait why does below import work
from polls import views as poll_views

#Allows referencing other URLconfs, which map URL patterns to views
urlpatterns = [
    path('', poll_views.reg_user, name='register_me'),
    path('userLogout/', poll_views.log_me_out, name='log_me_out'),
    path('accounts/', include('django.contrib.auth.urls')), #Apparently has associated auth views, so we just need to make tamplates apparently
    path('polls/', include('polls.urls')), #Allows referencing other URLconfs, which map URL patterns to views
    path('admin/', admin.site.urls),
]
