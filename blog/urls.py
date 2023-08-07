from django.urls import path
from blog import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('slug/<str:slug>', views.blogPost, name='blogPost'),
    path('postComment/', views.postComment, name="postComment")
]
