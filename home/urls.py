from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('signup/', views.handlesignup, name='handlesignup'),
    path('login/', views.handlelogin, name='handlesignup'),
    path('logout/', views.handlelogout, name='handlesignup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addBlog/', views.addBlog, name='addBlog'),
    path('<str:slug>/editBlog/', views.editBlog, name='editBlog'),
    path('profile/', views.profile, name='profile'),
    path('viewBlogs/', views.viewBlogs, name='viewBlogs')
]
