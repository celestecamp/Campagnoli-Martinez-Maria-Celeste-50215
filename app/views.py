from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

# Create your views here.
def home(request):
    etiqueta_destacado = Etiqueta.objects.get(tag="Destacado")
    
    # Obtener los productos que tienen la etiqueta "destacado"
    contexto = Producto.objects.filter(etiquetas=etiqueta_destacado)

    return render(request, 'app/index.html', {'productos_destacados': contexto})

#________________________________________LOGIN/LOGOUT/REGISTRATION
def login_request(request):
    if request.method == "GET":
        miForm = AuthenticationForm()
        return render(request, "app/login.html", {"form": miForm})
    
    else:
        usuario = request.POST['username']
        psw = request.POST['password']
        user = authenticate(request, username=usuario, password=psw)

        if user is not None:
            login(request, user)
            #___Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "images/avatares/default.jpg"
            finally:
                request.session["avatar"] = avatar

            return redirect(reverse_lazy('home'))
        else:
            return redirect(reverse_lazy('login'))

def register_request(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home'))
        return render(request, "app/registro.html", {"form": form})
    
    else:
        form = RegistroForm()
        return render(request, "app/registro.html", {"form": form})


#_____________________________________________PRODUCTO
def detalle_producto(request, producto_id):
    contexto = Producto.objects.get(pk=producto_id)
    comentarios = Comentario.objects.filter(producto=producto_id)
    return render(request, 'app/producto.html', {'p': contexto, 'comentarios': comentarios, 'user': request.user})

@login_required
def compra(request, producto_id):
    contexto = Producto.objects.get(pk=producto_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            return redirect (reverse_lazy('compra_fin'))
    else:
        form = CompraForm()

    return render(request, 'app/compra_realizar.html', {'p': contexto, 'form': form})

@login_required
def compra_fin(request):
    return render(request, 'app/compra_fin.html')

#___COMENTARIOS
@login_required
def comentar(request, producto_id):
    contexto = Producto.objects.get(pk=producto_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.avatar = Avatar.objects.get(user=request.user)
            comentario.producto = contexto
            comentario.save()
            return redirect('detalle_producto', producto_id=producto_id)
    
    else:
        form = CommentForm()

    return render(request, 'app/comentar.html', {'producto': contexto, 'form': form})

@login_required
def editar_comentario(request, comentario_id, producto_id):
    comentario = Comentario.objects.get(id=comentario_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect ('detalle_producto', producto_id=producto_id)
    else:
        form = CommentForm(instance=comentario)

    return render(request, 'app/comentar.html', {'form': form})

@login_required
def borrar_comentario(request, comentario_id, producto_id):
    comentario = Comentario.objects.get(id=comentario_id)
    comentario.delete()
    return redirect('detalle_producto', producto_id=producto_id)

#_____________________________________________EXPLORACIÓN
#Todo
def productos_todos(request):
    contexto1 = Producto.objects.all()
    contexto2 = Etiqueta.objects.all().order_by('tag')

    desde_etiquetas_view = False    #para el if que muestra los botones de filter y search

    return render(request, 'app/productoList.html', {'productos': contexto1,
                                                     'etiquetas': contexto2,
                                                     'desde_etiquetas_view': desde_etiquetas_view})

def productos_filtrados_tipo(request, tipo):
    contexto = Producto.objects.filter(tipo=tipo)
    return render(request, 'app/productoList.html', {'productos': contexto})

def productos_filtrados_etiqueta(request, etiqueta_tag):
    etiqueta = Etiqueta.objects.get(tag=etiqueta_tag)
    contexto = etiqueta.producto_set.all()

    desde_etiquetas_view = True #para decir que está entrando desde esta view y que no muestre los botones de filtrar/buscar

    return render(request, 'app/productoList.html', {'productos': contexto, 'desde_etiquetas_view': desde_etiquetas_view})


#Determinada categoría (y su función BUSCAR integrada)
def productos_por_categoria(request, tipo):
    patron = request.GET.get("buscar")
    if patron:
        contexto = Producto.objects.filter(tipo=tipo, nombre__icontains=patron)
    else:
        contexto = Producto.objects.filter(tipo=tipo)

    return render(request, 'app/productosCategoria.html', {'productos': contexto, 'categoria_actual': tipo})


#____________BUSCAR en TODOS LOS PRODUCTOS
def buscar(request):
    patron = request.GET.get("buscar")

    if patron:  # si el patrón no está vacío
        productos = Producto.objects.filter(nombre__icontains=patron)

    else:
        productos = Producto.objects.all()

    return render(request, "app/productoList.html", {"productos": productos})


#_____________________________________Administrador
@user_passes_test(lambda u: u.is_superuser)
def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('lista_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'app/nuevo_producto.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect ('detalle_producto', producto_id=id_producto)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'app/nuevo_producto.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def borrar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    producto.delete()
    return redirect('lista_productos')

#____ETIQUETAS
@user_passes_test(lambda u: u.is_superuser)
def nueva_etiqueta(request):
    if request.method == 'POST':
        form = etiquetaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('lista_productos')
    else:
        form = etiquetaForm()
    
    return render(request, 'app/nueva_etiqueta.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def editar_etiqueta(request, id_etiqueta):
    etiqueta = Etiqueta.objects.get(id=id_etiqueta)
    if request.method == 'POST':
        form = etiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect ('lista_productos')
    else:
        form = etiquetaForm(instance=etiqueta)

    return render(request, 'app/nueva_etiqueta.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def borrar_etiqueta(request, id_etiqueta):
    etiqueta = Etiqueta.objects.get(id=id_etiqueta)
    etiqueta.delete()
    return redirect('lista_productos')


#_____________________________________Avatar/Perfil
@login_required
def EditProfileView(request):
    usuario = request.user
    if request.method == "POST":
        Form = UserEditForm(request.POST, instance=usuario)
        if Form.is_valid():
            user = User.objects.get(username=usuario)
            user.email = Form.cleaned_data.get("email")
            user.nombre = Form.cleaned_data.get("nombre")
            user.apellido = Form.cleaned_data.get("apellido")
            user.save()
            return redirect(reverse_lazy('home'))
    else:
        Form = UserEditForm(instance=usuario)

    return render(request, "app/editar_perfil.html", {"form": Form} )  
    
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "app/psw_change.html"
    success_url = reverse_lazy('home')

def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = User.objects.get(username=request.user)

            avatar_viejo = Avatar.objects.filter(user=usuario)
            if len(avatar_viejo) > 0:
                for i in range (len(avatar_viejo)):
                    avatar_viejo[i].delete()

            avatar = Avatar(user=usuario, imagen=form.cleaned_data["imagen"])
            avatar.save()

            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            return redirect(reverse_lazy('home'))
    else:
        form = AvatarForm()
    
    return render(request, "app/agregar_avatar.html", {"form": form})


#__________Otras opciones del menú
def faqs(request):
    return render(request, 'app/faqs.html')

def acerca_de(request):
    return render(request, "app/acercade.html")