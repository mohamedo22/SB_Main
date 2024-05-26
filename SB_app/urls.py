from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.conf.urls import handler404
handler404 = custom_page_not_found_view
urlpatterns = [
    path('' , index , name='index'),
    path('SignUp/' , signUp , name='signUp' ),
    path('confirmEmail/' , confirmEmail , name='confirmEmail'),
    path('signIn/' , signIn , name='signIn'),
    path('home/withDraw/' , withdraw , name='withdraw' ),
    path('home/transfer/' , transfer , name='transfer' ),
    path('home/deposite/' , deposite , name='deposite' ),
    path('home/' , home , name='home' ),
    path('home/profile' , profile , name='profile' ),
]