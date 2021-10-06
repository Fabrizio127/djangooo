from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = { k:"" for k in fields }

class Prodform(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre_producto','precio','imgProducto','descuento')

class ProdDes(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('descuento',)