
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.messages import get_messages

from .forms import PacienteForm, LoginForm, DatosPacienteForm, PacienteFotoForm
from .models import Paciente, RegistroComida
from .decorators import paciente_login_required

@paciente_login_required
def home(request):
    return render(request, "home.html")

def inicio(request):
    return render(request, "inicio.html")


def register_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()  # Guarda el nuevo paciente en la base de datos

            # Guarda el ID del paciente en la sesión para autenticar
            request.session['paciente_id'] = paciente.id
            messages.success(request, f'Bienvenido, {paciente.nombre}!')

            # Redirige a la vista de perfil si es profesional
            if paciente.es_profesional:
                return redirect('miperfil')  
            
            # Redirige a la vista de datos del paciente si no es profesional
            return redirect('datos_paciente')  
    else:
        form = PacienteForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                paciente = Paciente.objects.get(email=email)
                if check_password(password, paciente.password):
                    # Guarda el ID del paciente en la sesión para indicar que está autenticado
                    request.session['paciente_id'] = paciente.id
                    messages.success(request, f'Bienvenido, {paciente.nombre}.')

                    # Verifica si el paciente es profesional y redirige a "mi_perfil"
                    if paciente.es_profesional:
                        return redirect('miperfil')

                    # Si no es profesional, redirige a la página de inicio
                    return redirect('home')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Paciente.DoesNotExist:
                messages.error(request, 'El correo electrónico no está registrado.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()  # Limpia toda la sesión
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')


@paciente_login_required
def consulta(request):
    return render(request, "consulta.html")

@paciente_login_required
def registro(request):
    return render(request, "registro.html")

@paciente_login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Renderizar el template para el email
        template = render_to_string('email-template.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        })

        emailSender = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['nutribalanceoficial@gmail.com']
        )
        emailSender.content_subtype = 'html'
        emailSender.fail_silently = False
        emailSender.send()

        # Agregar mensaje de éxito
        messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')

        # Consumir los mensajes para limpiar la cola
        storage = get_messages(request)
        for _ in storage:
            pass

        return redirect('consulta')  # Redirige a la página de consulta

    return render(request, 'contact.html')


def datos_paciente_view(request):
    paciente = Paciente.objects.get(id=request.session['paciente_id'])  # Obtiene el paciente logueado

    if request.method == 'POST':
        form = DatosPacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()  # Guarda los datos adicionales en el perfil del paciente
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = DatosPacienteForm(instance=paciente)

    return render(request, 'datospaciente.html', {'form': form, 'nombre': paciente.nombre})

def mi_perfil(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        # Si no hay paciente_id en la sesión, redirige al login
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')

    try:
        # Intenta obtener el paciente de la base de datos
        paciente = Paciente.objects.get(id=paciente_id)
    except Paciente.DoesNotExist:
        messages.error(request, "No se encontró el paciente en la base de datos.")
        return redirect('login')

    return render(request, 'mi_perfil.html', {'paciente': paciente})

def editar_perfil(request, id):
    paciente = get_object_or_404(Paciente, id=id)  # Obtiene el paciente por ID

    if request.method == 'POST':
        form = DatosPacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('miperfil')  # Redirige a la página de perfil después de guardar
    else:
        form = DatosPacienteForm(instance=paciente)

    return render(request, 'editar_perfil.html', {'form': form, 'paciente': paciente})

def editar_foto(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteFotoForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('miperfil')  # Cambia a la vista de perfil
    else:
        form = PacienteFotoForm(instance=paciente)
    return render(request, 'editar_foto.html', {'form': form, 'paciente': paciente})

@csrf_exempt
def editar_foto_ajax(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = PacienteFotoForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            paciente = form.save()
            return JsonResponse({'nueva_foto_url': paciente.foto_perfil.url}, status=200)
        else:
            return JsonResponse({'error': 'Formulario no válido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def editar_perfil_ajax(request, id):
    if request.method == 'POST':
        paciente = get_object_or_404(Paciente, id=id)
        form = DatosPacienteForm(request.POST, instance=paciente)

        if form.is_valid():
            paciente = form.save()
            # Devuelve los datos actualizados como JSON
            return JsonResponse({
                'edad': paciente.edad,
                'peso': paciente.peso,
                'altura': paciente.altura,
                'sexo': paciente.sexo,
            })

        # Si el formulario no es válido
        return JsonResponse({'error': 'Formulario no válido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def guardar_comida(request):
    if request.method == "POST":
        paciente_id = request.session.get('paciente_id')  # Obtén el ID del paciente desde la sesión
        if not paciente_id:
            # Si no hay paciente_id en la sesión, redirige a la página de registro
            messages.error(request, "Debes registrarte o iniciar sesión para registrar una comida.")
            return redirect('registro')

        try:
            # Obtén el paciente desde la base de datos
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            messages.error(request, "Paciente no encontrado.")
            return redirect('registro')

        # Obtén los datos enviados en el formulario
        imagen = request.FILES.get('imagen')
        emocion = request.POST.get('emocion')

        # Crea el registro de comida
        RegistroComida.objects.create(
            paciente=paciente,
            imagen=imagen,
            emocion=emocion
        )
        messages.success(request, "Registro de comida guardado exitosamente.")
        return redirect('registro')  # R


def historial_comidas(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        messages.error(request, "Debes registrarte o iniciar sesión para ver el historial de comidas.")
        return redirect('registro')

    try:
        paciente = Paciente.objects.get(id=paciente_id)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente no encontrado.")
        return redirect('registro')

    registros = RegistroComida.objects.filter(paciente=paciente).order_by('-fecha')
    return render(request, 'historial_comidas.html', {'registros': registros})

def registro(request):
    paciente_id = request.session.get('paciente_id')
    registros = []

    if paciente_id:
        try:
            paciente = Paciente.objects.get(id=paciente_id)
            # Obtener los registros de comidas del paciente
            registros = RegistroComida.objects.filter(paciente=paciente).order_by('-fecha')
        except Paciente.DoesNotExist:
            messages.error(request, "Paciente no encontrado.")
    else:
        messages.error(request, "Debes registrarte o iniciar sesión para acceder al historial.")

    # Renderiza el template con los registros
    return render(request, "registro.html", {'registros': registros})

def lista_pacientes(request):
    # Verifica que el usuario autenticado sea un profesional
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return redirect('login')  # Redirige al login si no está autenticado
    
    paciente_actual = get_object_or_404(Paciente, id=paciente_id)
    if not paciente_actual.es_profesional:
        return redirect('login')  # Redirige al login si no es un profesional

    pacientes = Paciente.objects.filter(es_profesional=False)  # Filtra solo pacientes no profesionales
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})

def acceder_cuenta(request, paciente_id):
    # Verifica que el usuario autenticado sea un profesional
    profesional_id = request.session.get('paciente_id')
    if not profesional_id:
        return redirect('login')  # Redirige al login si no está autenticado
    
    profesional_actual = get_object_or_404(Paciente, id=profesional_id)
    if not profesional_actual.es_profesional:
        return redirect('login')  # Redirige al login si no es un profesional

    # Obtiene al paciente que se desea impersonar
    paciente = get_object_or_404(Paciente, id=paciente_id)
    request.session['impersonar_usuario'] = paciente.id  # Guarda la sesión del usuario impersonado
    return redirect('perfil_paciente')  # Redirige al perfil del paciente impersonado

def perfil_paciente(request):
    # Verifica si hay un usuario impersonado
    paciente_id = request.session.get('impersonar_usuario')
    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
    else:
        # Si no hay impersonación, muestra el perfil del usuario actual
        paciente_id = request.session.get('paciente_id')
        if not paciente_id:
            return redirect('login')  # Redirige al login si no hay usuario autenticado
        paciente = get_object_or_404(Paciente, id=paciente_id)

    return render(request, 'mi_perfil.html', {'paciente': paciente})

def salir_impersonacion(request):
    if 'impersonar_usuario' in request.session:
        del request.session['impersonar_usuario']  # Elimina la sesión del usuario impersonado
    return redirect('lista_pacientes')  # Redirige a la lista de pacientes














