from rest_framework.fields import ReadOnlyField
from .models import Producto, categoria, subcategoria
from rest_framework import serializers

class CategoriaSerializer(serializers.ModelSerializer):
    
    NombreCategoria = serializers.CharField(required=True)

    class Meta:
         model=categoria
         fields='__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):
    
    Nombresubcategoria = serializers.CharField(required=True)
    
    
    class Meta:
         model= subcategoria
         fields='__all__'



class ProductoSerializer(serializers.ModelSerializer):
    
    nombre_categoria = serializers.CharField(read_only=True, source="categoria.NombreCategoria")
    nombre_subcategoria = serializers.CharField(read_only=True, source="subcategoria.Nombresubcategoria")
    nombre_producto = serializers.CharField(required=True)
    precio = serializers.IntegerField(required=True)
    imgProducto = serializers.ImageField(required=True)

    def validate_nombre_producto(self, value):
        existe = Producto.objects.filter(nombre_producto__iexact=value).exists()

        if existe:
            raise serializers.ValidationError("Este producto ya existe")
        return value
    
    class Meta:
         model=Producto
         fields='__all__'
