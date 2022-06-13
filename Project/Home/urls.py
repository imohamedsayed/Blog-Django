from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('home', views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('singup',views.singup,name='singup'),
    path('singin',views.singin,name='singin'),
    path('logout',views.logout,name='logout'),
    path('search',views.search,name='search'),
    path('post/<int:post_id>',views.post_single,name='single_post'),
    path('categories_post/<int:cat_id>',views.cat_post,name='cat_post'),
    path('change_password',views.change_pass,name='change_password')
]