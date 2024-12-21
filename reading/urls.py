from django.contrib import admin
from django.urls import path
from reading import views

urlpatterns = [
    path('',views.main,name='main'),
    path('home/',views.home,name='home'),
    path('kyeword/',views.kyeword,name='kyeword'),


path('readinginput/', views.readinginput, name='readinginput'),
path('readingtranslator/', views.readingtranslator, name='readingtranslator'),
path('translate_word_ajax/', views.translate_word_ajax, name='translate_word_ajax'),



   
    ]



