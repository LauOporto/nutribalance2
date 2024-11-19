from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import editar_foto_ajax
from .views import editar_perfil_ajax

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), # Ruta para el escaneo de puertos
    path('inicio/', views.inicio, name='inicio'),
    path('mi_perfil/', views.mi_perfil, name='miperfil'),
    path('registro/', views.registro, name='registro'),
    path('consulta/', views.consulta, name='consulta'),
    path('contact', views.contact, name='contact'),
    path('datos_paciente/', views.datos_paciente_view, name='datos_paciente'),
    path('editar-perfil/<int:id>/', views.editar_perfil, name='editar_perfil'),
    path('editar_foto/<int:paciente_id>/', views.editar_foto, name='editar_foto'),
    path('editar_foto_ajax/<int:paciente_id>/', editar_foto_ajax, name='editar_foto_ajax'),
    path('editar_perfil_ajax/<int:id>/', editar_perfil_ajax, name='editar_perfil_ajax'),
    path('guardar-comida/', views.guardar_comida, name='guardar_comida'),
    path('historial-comidas/', views.historial_comidas, name='historial_comidas'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/acceder/<int:paciente_id>/', views.acceder_cuenta, name='acceder_cuenta'),
    path('perfil/', views.perfil_paciente, name='perfil_paciente'),
    path('salir-impersonacion/', views.salir_impersonacion, name='salir_impersonacion'),
    
]

if settings.DEBUG:  # Sirve los archivos de medios solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)