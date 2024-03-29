from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CompraForm(forms.Form):
    dni_cuit_cuil = forms.CharField(max_length=20, required=True, label='DNI/CUIT/CUIL')
    codigo_postal = forms.CharField(max_length=10, required=True, label='Código Postal')
    provincia = forms.CharField(max_length=50, required=True)

    PAGO_CHOICES = (
        ('Transferencia', 'Transferencia'),
        ('Crédito', 'Crédito'),
        ('Débito', 'Débito'),
    )
    pago = forms.ChoiceField(choices=PAGO_CHOICES, label='Método de pago')

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=50, required=True, label="Nombre/s")
    apellido = forms.CharField(max_length=70, required=True, label="Apellido/s")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "nombre", "apellido", "email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data["nombre"]
        user.apellido = self.cleaned_data["apellido"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserEditForm(UserChangeForm):
    nombre = forms.CharField(max_length=50, required=True, label="Nombre/s")
    apellido = forms.CharField(max_length=70, required=True, label="Apellido/s")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["nombre", "apellido", "email"]


#__________________CRUDs DE LOS MODELOS__________________
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'etiquetas', 'descripcion', 'tipo', 'imagen', 'precio']

        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 25, 
                                                 'rows': 4}), # Cambiar el tamaño del campo de texto
        }

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)

class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=1000, required=True, label="Comentar")
    
    class Meta:
        model = Comentario
        fields = ["comment",]
        widgets = {'comment': forms.Textarea(attrs={'cols': 25,
                                                    'rows': 4})}

class etiquetaForm(forms.ModelForm):
    tag = forms.CharField(max_length=20, label="Nombre de la etiqueta:")

    class Meta:
        model = Etiqueta
        fields = ["tag",]

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        capitalized_tag = tag.capitalize()
        return capitalized_tag