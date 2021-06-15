from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),


    path('logout/', views.logout, name='logout'),


    path('question/<int:pk>/', views.single_question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('', views.index, name='index')
]
