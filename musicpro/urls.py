from django.urls import path , include
from django.contrib.auth.views import LoginView , LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewset)
router.register('categoria', CategoriaViewset)
router.register('subcategoria', SubCategoriaViewset)


urlpatterns = [
    path('', views.index, name='index'),
    path('CompraF.html', views.CompraF, name='CompraF.html'),
    path('index.html', views.index, name='index.html'),
    path('Destacados.html', views.destacados, name='Destacados.html'),
    path('catalogo.html', views.catalogo, name='catalogo.html'),
    path('login',LoginView.as_view(template_name = 'musicpro/login.html'), name="login"),
    path('logout/',LogoutView.as_view(template_name = 'musicpro/index.html'), name="logout"),
    path('register/',views.register,name="register"),
    path('add_product_carrito/<int:product_id>/', add_product_carrito, name='add_product_carrito'),
    path('add_product_catalogo/<int:product_id>/', add_product_catalogo, name='add_product_catalogo'),
    path('remove_product/<int:product_id>/', remove_product, name='remove_product'),
    path('decrement_product/<int:product_id>/', decrement_product, name='decrement_product'),
    path('producto_edit.html/<id>/', modificar_producto, name="modificar_producto"),
    path('agregar_descuento.html/<id>/', agregar_descuento, name="agregar_descuento"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('clear/', clear_cart, name='clear_cart'),
    path('carrito.html', views.webpay),
    path('terminar.html', views.webpaycommit),
    path('reembolso.html', views.webpayplus_reembolso),
    path('anular.html', views.webpayplus_anular),
    path('api/', include(router.urls)),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
