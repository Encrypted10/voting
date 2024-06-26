"""
URL configuration for voting_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from elections import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path("aboutus/", views.aboutus, name="aboutus"),
    path('',views.landingpage, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home, name='home'),
    path('footer/', views.footerpage, name='footer'),

    path('nominees/', views.nominees, name='nominees'),
    path('cast/', views.cast_vote, name='cast_vote'),
    path('results/', views.results, name='results'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_nominee/', views.add_nominee, name='add_nominee'),
    path('add_user/', views.add_user, name='add_user'),
]
