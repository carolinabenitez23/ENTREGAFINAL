
from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.forms import ProfesorFormulario, CursoFormulario, EstudianteFormulario, BuscarCursoFormulario, LoginForm, AvatarFormulario, UserEditForm # Importar AvatarFormulario y UserEditForm
from AppCoder.models import Curso, Estudiante
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm





def inicio(request):
    return render(request, "AppCoder/inicio.html")



def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorFormulario(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = ProfesorFormulario()
    return render(request, "AppCoder/formulario.html", {"form": form, "titulo": "Crear Profesor"})



def crear_curso(request):
    if request.method == 'POST':
        form = CursoFormulario(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = CursoFormulario()
    return render(request, "AppCoder/formulario.html", {"form": form, "titulo": "Crear Curso"})



def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppCoder:estudiantes') 
    else:
        form = EstudianteFormulario()
    return render(request, "AppCoder/formulario.html", {"form": form, "titulo": "Crear Estudiante"})



def buscar_curso(request):
    cursos = []
    if request.GET.get('nombre'):
        nombre = request.GET['nombre']
        cursos = Curso.objects.filter(nombre__icontains=nombre)
    form = BuscarCursoFormulario()
    return render(request, "AppCoder/buscar.html", {"form": form, "resultados": cursos})




def estudiantes(request):
    estudiantes = Estudiante.objects.all()
   
    for est in estudiantes:
        print(f"DEBUG: Estudiante ID: {est.id}, Nombre: {est.nombre}, Tipo: {type(est.id)}")
  
    dicc = {"estudiantes": estudiantes}
    return render(request, "AppCoder/estudiantes.html", dicc)


@login_required
def eliminar_estudiante(request, id):
    try:
        estudiante = Estudiante.objects.get(id=id)
        estudiante.delete()
        return redirect('AppCoder:estudiantes')  
    except Estudiante.DoesNotExist:
        return HttpResponse("Estudiante no encontrado")
    except Exception as e:
        return HttpResponse(f"Error al eliminar el estudiante: {e}")
    

@login_required
def editar_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    if request.method == 'POST':
        form = EstudianteFormulario(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('AppCoder:estudiantes')
    else:
        form = EstudianteFormulario(instance=estudiante)
    return render(request, "AppCoder/formulario.html", {"form": form, "titulo": "Editar Estudiante"})





def login_view(request):

    print("GET next:", request.GET.get('next'))
    print("POST next:", request.POST.get('next'))
    
    
    next_url = request.GET.get('next') or request.POST.get('next') or '/AppCoder/'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)  
            else:
                error_message = "Credenciales inválidas"
        else:
            error_message = "Formulario inválido"
    else:
        form = LoginForm()
        error_message = None

    return render(request, "AppCoder/login.html", {
        "form": form,
        "error_message": error_message,
        "next": next_url  
    })




def register(request):    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('AppCoder:inicio')  
    else:
        form = UserCreationForm()

    return render(request, "AppCoder/register.html", {"form": form})




def logout_view(request):
    logout(request)
    return redirect('AppCoder:inicio')


@login_required
def editar_perfil(request):
    usuario = request.user
    print(f"DEBUG: User - Username: {usuario.username}, Email: {usuario.email}, First Name: {usuario.first_name}, Last Name: {usuario.last_name}")
    estudiante_profile, created = Estudiante.objects.get_or_create(user=usuario)
    print(f"DEBUG: Estudiante Profile - Created: {created}, Avatar: {estudiante_profile.avatar}")

    if request.method == 'POST':
        form_user = UserEditForm(request.POST, instance=usuario)
        form_avatar = AvatarFormulario(request.POST, request.FILES, instance=estudiante_profile)

        if form_user.is_valid() and form_avatar.is_valid():
            form_user.save()
            form_avatar.save()
            return redirect('AppCoder:inicio')  
    else:
        form_user = UserEditForm(instance=usuario)
        form_avatar = AvatarFormulario(instance=estudiante_profile)

    return render(request, 'AppCoder/editar_perfil.html', {'form_user': form_user, 'form_avatar': form_avatar, 'titulo': 'Editar Perfil'})


