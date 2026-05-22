from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'create/',
        views.create_post,
        name='create'
    ),

    path(
        'update/<int:pk>/',
        views.update_post,
        name='update'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_post,
        name='delete'
    ),

    path(
        'post/<int:pk>/',
        views.post_detail,
        name='detail'
    ),
]