from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # PARA NO AÑADIR /APP/ A LA RUTA
    path('', views.home_redirect),

    # PAGINA INDEX
    path('index/', views.index_load, name="index_load"),

    # LOGIN
    path('accounts/login', views.do_login, name="login"),
    path('accounts/logout', views.do_logout, name="logout"),
    path('accounts/register', views.do_register, name="register"),

    # PROFILE
    path('profiles/profile', views.profile_create, name="profile"),

    # CRUD PRODUCTS
    path('products/', views.product_list, name="product_list"),
    path('products/new', views.product_new, name="product_new"),
    path('products/<int:id>/load', views.product_load, name="product_load"),
    path('products/filter/', views.product_filter, name="product_filter"),
    path('products/save', views.product_save, name="product_save"),
    path('products/<int:id>/view', views.product_view, name="product_view"),
    path('products/<int:pk>/delete', views.product_delete, name='product_delete'),

    # MANUFACTURERS
    path('manufacturers/', views.manufacturer_list, name="manufacturer_list"),

    # LINKS FOOTER
    path('pages/politica_privacidad', views.politica_privacidad, name="politica_privacidad"),
    path('pages/aviso_legal', views.aviso_legal, name="aviso_legal"),
    path('pages/politica_cookies', views.politica_cookies, name="politica_cookies"),
    path('pages/formas_de_pago', views.formas_de_pago, name="formas_de_pago"),
    path('pages/logistica_y_envios', views.logistica_y_envios, name="logistica_y_envios"),
    path('pages/quien_somos', views.quien_somos, name="quien_somos"),
    path('pages/garantias_devoluciones', views.garantias_devoluciones, name="garantias_devoluciones"),
    path('pages/financiacion', views.financiacion, name="financiacion"),

    # CRUD CART
    path('cart/<int:product_id>/add', views.cart_add_product, name="cart_add_product"),
    path('cart/<int:product_id>/clean', views.cart_clean, name="cart_clean"),

    # VIEW CART
    path('cart/', views.cart_view, name="cart_view"),

    # CART ADD TABLE
    path('cart/<int:product_id>/plus', views.cart_add_table, name="cart_add_table"),

    # CART DEDUCT TABLE
    path('cart/<int:product_id>/deduct', views.cart_deduct_table, name="cart_deduct_table"),

    # CART DELETE TABLE
    path('cart/<int:product_id>/delete', views.cart_delete_table, name="cart_delete_table"),

    # CART SAVE
    path('cart/save', views.cart_save, name="cart_save"),

]



