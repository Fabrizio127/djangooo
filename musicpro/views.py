import random
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.conf.urls.static import static
from django.utils import timezone
from .models import Producto, categoria, subcategoria
from .cart import Cart
from .context_processor import cart_total_amount
from .forms import Prodform,ProdDes
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transbank_error import TransbankError
from rest_framework import viewsets
from .serializers import ProductoSerializer, CategoriaSerializer, SubCategoriaSerializer

# Create your views here.

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre_producto')

        if nombre:
            productos = productos.filter(nombre_producto__contains=nombre)
        return productos

class CategoriaViewset(viewsets.ModelViewSet):
    queryset = categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        categorias = categoria.objects.all()
        nombre = self.request.GET.get('NombreCategoria')

        if nombre:
            categorias = categorias.filter(NombreCategoria__contains=nombre)
        return categorias

class SubCategoriaViewset(viewsets.ModelViewSet):
    queryset = subcategoria.objects.all()
    serializer_class = SubCategoriaSerializer

    def get_queryset(self):
        subcategorias = subcategoria.objects.all()
        nombre = self.request.GET.get('Nombresubcategoria')

        if nombre:
            subcategorias = subcategorias.filter(Nombresubcategoria__contains=nombre)
        return subcategorias



@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = { 'form': form }
    return render(request, 'musicpro/register.html',context)

@csrf_protect
def index(request):
    cart = Cart(request)
    return render(request, 'musicpro/index.html', {})
@csrf_protect
def destacados(request):
    cart = Cart(request)
    return render(request, 'musicpro/destacados.html', {})
@csrf_protect
def catalogo(request):
    products = Producto.objects.all()
    cart = Cart(request)
    form = Prodform()
    if request.POST.get('marca'):
        if request.method == "POST":
            form = Prodform(request.POST, request.FILES)
            if form.is_valid():
                ProdAgre = form.save(commit=False)
                ProdAgre.nombre_producto = request.POST.get('nombre_producto')
                ProdAgre.imgProducto = form.cleaned_data['imgProducto']
                ProdAgre.save()
                return redirect('catalogo.html')
    else:
            products = Producto.objects.all()
            return render(request, "musicpro/catalogo.html", {
            "products": products,'form': form,})





@csrf_protect
def loggin(request):
    cart = Cart(request)
    return render(request, 'musicpro/loggin.html')
@csrf_protect
def CompraF(request):
    cart = Cart(request)
    return render(request, 'musicpro/CompraF.html')

@csrf_protect
def add_product_catalogo(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.add(product=product)
    return redirect("/catalogo.html")


def add_product_carrito(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.add(product=product)
    return redirect("/carrito.html")




@csrf_protect
def remove_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.remove(product)
    return redirect("/carrito.html")


@csrf_protect
def decrement_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.decrement(product=product)
    return redirect("/carrito.html")


@csrf_protect
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/carrito.html")
@csrf_protect
def modificar_producto(request, id):
    cart = Cart(request)
    prod = Producto.objects.get(id = id)
    if request.method == 'POST':
        product = Prodform(request.POST, instance = prod)
        if product.is_valid():
            prod = product.save(commit=False)
            prod.save()
            return redirect('catalogo.html')
    else:
        cart = Cart(request)
        product = Prodform(instance= prod)    
        return render(request, 'musicpro/producto_edit.html',{'product':product})
@csrf_protect
def agregar_descuento(request, id):
    cart = Cart(request)
    prod = Producto.objects.get(id = id)
    if request.method == 'POST':
        product = ProdDes(request.POST, instance = prod)
        if product.is_valid():
            prod = product.save(commit=False)
            prod.save()
            return redirect('catalogo.html')
    else:
        cart = Cart(request)
        product = ProdDes(instance= prod)    
        return render(request, 'musicpro/producto_desc.html',{'product':product,'prod':prod})
       
@csrf_protect
def eliminar_producto(request, id):
    cart = Cart(request)
    product = Producto.objects.get(id=id)
    try:
        product.delete()
        mensajes = "Eliminado correctamente"
        messages.success(request, mensajes)
        return redirect('catalogo.html')
    except:
        cart = Cart(request)
        mensaje = "No se a eliminado el archibo seleccionado"
        messages.error(request, mensaje)
    return redirect('catalogo')
    
def webpay(request):
    total = 0
    FprecioC = 0
    cart = Cart(request)
    buy_order = str(1)
    session_id = str(1)
    return_url = 'http://127.0.0.1:8000/terminar.html'
    total = 0
    FprecioC = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price']) * value['quantity'])
            # FprecioC=(f'{total:.3f}')
            FprecioC= int(total)
    amount = FprecioC
    try:
        response = Transaction().create(buy_order, session_id, amount, return_url)
        print(amount)
        return render(request, 'musicpro/carrito.html', {"response":response})
    except TransbankError as e:
        print(e.message)
        return render(request, 'musicpro/carrito.html', {})


def webpaycommit(request):
    cart = Cart(request)
    token = request.POST.get("token_ws")
    response = Transaction().commit(token)     
    return render(request, 'musicpro/terminar.html',{"token": token,"response": response})
    

def webpayplus_reembolso(request):
    token = request.POST.get("token_ws")
    amount = request.POST.get("amount")
    try:
        response = Transaction().refund(token, amount)
        print(response)
        print(token)
        return render(request, 'musicpro/reembolso.html', {"token":token, "amount": amount, "response":response})
    except TransbankError as e:
        print(e.message)
    return render(request, 'musicpro/reembolso.html', {})

def webpayplus_anular(request):
    cart = Cart(request)
    return render(request, 'musicpro/anular.html', {})