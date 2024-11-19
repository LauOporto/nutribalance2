from django.shortcuts import redirect

def paciente_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('paciente_id'):
            return redirect('login')  # Redirige al login si no hay paciente en sesión
        return view_func(request, *args, **kwargs)
    return wrapper