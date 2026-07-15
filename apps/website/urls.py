from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("soluciones/", views.solutions, name="solutions"),
    path("soluciones/<slug:slug>/", views.solution_detail, name="solution_detail"),
    path("metodo/", views.method, name="method"),
    path("casos/", views.cases, name="cases"),
    path("nosotros/", views.about, name="about"),
    path("contacto/", views.contact, name="contact"),
    path("privacidad/", views.privacy, name="privacy"),
]
