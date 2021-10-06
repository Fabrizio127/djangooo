from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Perfil(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        direccion=models.CharField(max_length=50,null=True)
        ciudad=models.CharField(max_length=50,null=True) 
        país=models.CharField(max_length=50,null=True)
        def str(self):
                return f'Perfil de {self.user.username}'



class categoria(models.Model):
        NombreCategoria=models.CharField(max_length=50,null=True)
        def __str__(self):
                return self.NombreCategoria


class subcategoria(models.Model):
        Nombresubcategoria=models.CharField(max_length=50,null=True)
        categoria = models.ForeignKey(categoria, on_delete=models.CASCADE,null=True)
        def __str__(self):
                return "{Nombresubcategoria} ({categoria})".format(Nombresubcategoria=self.Nombresubcategoria, categoria=self.categoria.NombreCategoria)

class descuento(models.Model):
        descuentostr =models.CharField(max_length=50,null=True)
        descuento = models.IntegerField(default=0, null=True)
        def __str__(self):
                return self.descuentostr



class Producto(models.Model):
        nombre_producto =models.CharField(max_length=50,null=True)
        categoria = models.ForeignKey(categoria, on_delete=models.CASCADE,null=True)
        descuento = models.ForeignKey(descuento,default=0, on_delete=models.CASCADE,null=True)
        precio = models.IntegerField(default=0, null=True)
        subcategoria = models.ForeignKey(subcategoria, on_delete=models.CASCADE,null=True)
        imgProducto = models.ImageField(upload_to="imgproductos", null=True)
        def __str__(self):
                return self.nombre_producto
