

from django.urls import path
from . import views

app_name = 'AppCoder'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('profesor/', views.crear_profesor, name='crear_profesor'),
    path('curso/', views.crear_curso, name='crear_curso'),
    path('estudiante/', views.crear_estudiante, name='crear_estudiante'),
    path('buscar/', views.buscar_curso, name='buscar_curso'),
    path("estudiantes/", views.estudiantes, name="estudiantes"),
    path("eliminar_estudiante/<int:id>/", views.eliminar_estudiante, name="eliminar_estudiante"),
    path("editar_estudiante/<int:id>/", views.editar_estudiante, name="editar_estudiante"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("editar_perfil/", views.editar_perfil, name="editar_perfil"),
]

