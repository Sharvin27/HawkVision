from django.urls import path
from . import views

urlpatterns = [
    path("od", views.od, name='od'),
    path("ocr", views.ocr, name = 'ocr')
]