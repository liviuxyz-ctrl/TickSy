# """ticksy URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name="home_page"),
    path('about-us/', views.about_us, name="about_us_page"),
    path('create-ticket/', views.tickets_creator, name="ticket_creator_page"),
    path('tickets/', views.tickets_list, name="ticket_list_page"),
    path('contact/', views.contact_page, name="contact_page"),
    path('login/', views.login_page, name="login_page"),
    path('login-api/', views.login),
    path('login-api/logout_user=<str:logout_user>', views.login),
    path('user-state', views.request_login_state),
    path('register/', views.register, name="register_page"),
    path('register-api/', views.register),
    path('team/', views.register_team),
    path('team/lookup_team=<str:team_name>', views.lookup_team),
    path('ticket/', views.ticket)
]
