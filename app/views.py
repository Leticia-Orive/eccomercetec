from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Product, Category, Manufacturer, Profile, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# def home(request):
#     return render(request, "home.html")


def home_redirect(request):
    return HttpResponseRedirect("/products")


# ************** CARGA PAGINA DE INICIO ***************
def index_load(request):
    print(request.session.session_key)
    request.session["cart"] = []
    request.session["lists_products"] = []
    request.session["total_invoice"] = 0
    request.session["count_products"] = 0

    data = {
        "products": Product.objects.all(),
        "categories": Category.objects.all()
    }
    return render(request, "indice/index.html", context=data)
    #return HttpResponseRedirect("/indice")


# ************** SIGN IN / SIGN UP ***************

def do_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "accounts/login.html")

    login(request, user)
    return redirect('index_load')


def do_logout(request):
    logout(request)
    # NAME DEL PATH [ path('accounts/login', views.do_login, name="login")]
    return redirect('login')


def do_register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    User.objects.create_user(username, email, password)
    # NAME DEL PATH [ path('accounts/login', views.do_login, name="login")]
    return redirect('login')


# *************** CRUD PROFILE ***************


def profile_create(request):
    email_form = request.POST.get("email")
    type_form = request.POST.get("type")

    user = User.objects.get(email=email_form).first()

    Profile.objects.create(user.id, type_form)
    # return HttpResponseRedirect("/products")
    return redirect('/products')


# *************** CRUD PRODUCTOS ***************


@login_required
def product_list(request):
    data = {
        "products": Product.objects.all(),
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_list.html", context=data)


@login_required
def product_new(request):
    data = {
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_load(request, id):
    data = {
        "product": Product.objects.get(id=id),  # recuperamos el producto
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_save(request):
    creation = not request.POST.get("id")
    manufacturers = request.POST.getlist('manufacturers')

    category_id_str = request.POST.get("category_id")
    category_id = int(category_id_str) if category_id_str else None

    if creation:
        product = Product.objects.create(
            # manufacturer=request.POST.get("manufacturer"),
            model=request.POST.get("model"),
            ram=request.POST.get("ram"),
            description=request.POST.get("description"),
            price=float(request.POST.get("price")),
            image=request.POST.get("image"),
            category_id=category_id
        )
        product.manufacturers.set(manufacturers)
    else:
        # Editar un producto existente
        id_product = int(request.POST.get("id"))
        product = Product.objects.get(id=id_product)

        # product.manufacturer = request.POST.get("manufacturer")
        product.model = request.POST.get("model")
        product.ram = request.POST.get("ram")
        product.description = request.POST.get("description")
        product.price = float(request.POST.get("price"))
        product.image = request.POST.get("image")
        product.category_id = category_id
        product.manufacturers.set(manufacturers)

        product.save()
    return HttpResponseRedirect("/products/{}/view".format(product.id))


@login_required
def product_filter(request):
    category_id_str = request.GET.get("category_id")
    manufacturers = request.GET.getlist("manufacturers")
    category_id = int(category_id_str) if category_id_str else None

    products = None
    if category_id and len(manufacturers) >= 1:
        products = Product.objects.filter(category_id=category_id, manufacturers__id__in=manufacturers).distinct()
    elif category_id:
        products = Product.objects.filter(category_id=category_id)
    elif len(manufacturers) >= 1:
        products = Product.objects.filter(manufacturers__id__in=manufacturers).distinct()
    else:
        products = Product.objects.all()

    data = {
        "products": products,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        # Seleccionados en el filtro
        "category_id": category_id,
        "manufacturers_filtered": Manufacturer.objects.filter(id__in=manufacturers)
    }

    return render(request, "products/product_list.html", context=data)


@login_required
def product_view(request, id):
    product = Product.objects.get(id=id)
    data = {
        "product": product,
        "manufacturers": product.manufacturers.all()
    }
    return render(request, "products/product_view_card.html", context=data)
    #return render(request, "products/product_view.html", context=data)


@login_required
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return HttpResponseRedirect("/products")
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product no encontrado")


# *************** MANUFACTURER ***************


@login_required
def manufacturer_list(request):
    data = {
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "manufacturers/manufacturer_list.html", context=data)


########################## link footer ########################
def politica_privacidad(request):
    return render(request, "pages/politica_privacidad.html")

def aviso_legal(request):
    return render(request, "pages/aviso_legal.html")

def politica_cookies(request):
    return render(request, "pages/politica_cookies.html")

def formas_de_pago(request):
    return render(request, "pages/formas_de_pago.html")

def logistica_y_envios(request):
    return render(request, "pages/logistica_y_envios.html")

def quien_somos(request):
    return render(request, "pages/quien_somos.html")

def garantias_devoluciones(request):
    return render(request, "pages/garantias_devoluciones.html")

def financiacion(request):
    return render(request, "pages/financiacion.html")


# ************** OPERACIONES CARRITO DE COMPRA ***************

def cart_add_product(request, product_id):

    product = Product.objects.get(id=product_id)

    # lista = []
    lista = request.session["cart"]
    lista.append(product.id)
    print("cart add product")
    print(lista)
    request.session["cart"] = lista
    print("sesion :")
    print(request.session["cart"])

    # new code

    not_duplicated = list(set(lista))

    print("session list_products")
    print(request.session["lists_products"])
    request.session["lists_products"] = []

    lists_products = request.session["lists_products"]
    print("list_products")
    print(lists_products)

    # AQUI SE ALMACENA LOS OBJETOS [ PRODUCTOS -> DICCIONARIO ] EN BASE A LOS ID'S NO DUPLICADOS
    for id in not_duplicated:
        product = Product.objects.get(id=id)
        item = {
            "id": id,
            "model": product.model,
            "price": product.price,
            "quantity": lista.count(id),
            "subtotal": lista.count(id) * product.price
        }
        lists_products.append(item)
        # request.session["lists_products"] = []
        # request.session["lists_products"] = lists_products

    # AQUI MODIFICAMOS LA CANTIDAD DEL PRODUCTO QUE ES PASADO POR PARÁMETRO
    # for item in lists_products:  # lists_products:
    #    if item['id'] == product_id:
    #        item['quantity'] = item['quantity'] + 1
    #        item['subtotal'] = item['price'] * item['quantity']
    #        break

    request.session["lists_products"] = lists_products
    print("actualizo lists_products con producto añadido")
    print(request.session["lists_products"])

    total = 0
    count = 0

    for item in lists_products:  # lists_products:
        total = item['subtotal'] + total
        count = item['quantity'] + count

    request.session["total_invoice"] = total
    request.session["count_products"] = count

    # end new code

    data = {
        "products": Product.objects.all(),  # recupera productos de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        "lists": request.session["cart"]
    }

    return render(request, "products/product_list.html", context=data)


def cart_clean(request, product_id):
    pass


def cart_view(request):

    # PARA PINTAR EL CARRITO USAMOS [ request.session[lists_products ] ... LA ALMACENAMOS EN UNA VARIABLE LOCAL TEMPORAL

    lists_products = request.session["lists_products"]
    print("cart view list_products")
    print(lists_products)
    print("cart view list_products->sesion")
    print(request.session["lists_products"])

    # CALCULO EL VALOR TOTAL DEL "CART" Y LA CANTIDAD DEPRODUCTOS

    total = 0
    count = 0

    for item in lists_products:  # lists_products:
        total = item['subtotal'] + total
        count = item['quantity'] + count

    # EL VALOR TOTAL Y LA CANTIDAD TOTAL DE PRODUCTOS SE ALMACENA EN VARIABLES CREADAS EN REQUEST.SESSION
    request.session["total_invoice"] = total
    request.session["count_products"] = count

    # LE PASAREMOS LA DATA AL FICHERO "CART.HTML" QUIEN RENDERIZA LA INFORMACIÓN DEL "CART"
    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        "lists": request.session["cart"],
        "lists_products": request.session["lists_products"],
        "total": request.session["total_invoice"],
        "count": request.session["count_products"]
    }
    return render(request, "cart/cart.html", context=data)


def cart_add_table(request, product_id):

    # new codigo
    product = Product.objects.get(id=product_id)

    lista = request.session["cart"]
    lista.append(product.id)
    request.session["cart"] = lista

    # lists_products = request.session["lists_products"]

    not_duplicated = list(set(lista))

    request.session["lists_products"] = []
    lists_products = request.session["lists_products"]

    # AQUI SE ALMACENA LOS OBJETOS [ PRODUCTOS -> DICCIONARIO ] EN BASE A LOS ID'S NO DUPLICADOS
    for id in not_duplicated:
        product = Product.objects.get(id=id)
        item = {
            "id": id,
            "model": product.model,
            "price": product.price,
            "quantity": lista.count(id),
            "subtotal": lista.count(id) * product.price
        }
        lists_products.append(item)

    quantity_modified = 0
    subtotal_modified = 0
    indice = 0

    # AQUI MODIFICAMOS LA CANTIDAD DEL PRODUCTO QUE ES PASADO POR PARÁMETRO
    '''
    for item in lists_products:        # lists_products:
        if item['id'] == product_id:
            item['quantity'] = item['quantity'] + 1
            item['subtotal'] = item['price'] * item['quantity']
            break
    '''
    request.session["lists_products"] = lists_products

    total = 0
    count = 0

    for item in lists_products:  # lists_products:
        total = item['subtotal'] + total
        count = item['quantity'] + count

    request.session["total_invoice"] = total
    request.session["count_products"] = count

    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        "lists": request.session["cart"],
        "lists_products": request.session["lists_products"],
        "total": request.session["total_invoice"],
        "count": request.session["count_products"]
    }
    return render(request, "cart/cart.html", context=data)


def cart_deduct_table(request, product_id):

    lists_products = request.session["lists_products"]
    cart = request.session["cart"]
    print("cart deduct table")
    print(lists_products)

    quantity_modified = 0
    subtotal_modified = 0
    indice = 0

    for item in lists_products:        # lists_products:
        if item['id'] == product_id:
            if item['quantity'] > 0:
                # item['quantity'] = item['quantity'] - 1
                quantity_modified = item['quantity'] - 1
                # item['subtotal'] = item['price'] * item['quantity']
                subtotal_modified = item['price'] * quantity_modified
            if item['quantity'] == 0:
                pass
            break
        indice = indice + 1

    # ACTUALIZO EL CARRITO ... ELIMINO EL ID ESPECIFICADO
    cart.remove(product_id)
    request.session["cart"] = cart

    # PARA ACTUALIZAR LOS ATRIBUTOS DEL DICCIONARIO ES NECESARIO INVOCAR LAS CLAVES DESDE EL INDICE DE LA LISTA
    lists_products[indice]['quantity'] = quantity_modified
    lists_products[indice]['subtotal'] = subtotal_modified

    #ACTUALIZO [ lists_products ] ... NUESTRA LISTA GLOBAL QUE SE PINTARÁ EN EL CARRITO
    request.session["lists_products"] = lists_products

    # PARA EL CÁLCULO DEL TOTAL DE LA COMPRA Y EL TOTAL DE PRODUCTOS VENDIDOS
    total = 0
    count = 0

    for item in lists_products:        # lists_products:
        total = item['subtotal'] + total
        count = item['quantity'] + count

    request.session["total_invoice"] = total
    request.session["count_products"] = count

    # DATA QUE PASAREMOS AL HTML QUE RENDERIZARÁ LA INFO DEL CART [ cart.html ]
    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        "lists": request.session["cart"],
        "lists_products": request.session["lists_products"],
        "total": request.session["total_invoice"],
        "count": request.session["count_products"]
    }
    return render(request, "cart/cart.html", context=data)


def cart_delete_table(request, product_id):

    cart = request.session["cart"]
    lists_products = request.session["lists_products"]
    print("cart delete table")
    print(lists_products)

    indice = 0

    for item in lists_products:         # lists_products:
        if item['id'] == product_id:
            break
        indice = indice + 1

    print(indice)

    cart.count(product_id)
    print(cart.count(product_id))
    for i in range(0, cart.count(product_id)):         # lists_products:
        cart.remove(product_id)

    request.session["cart"] = cart

    del lists_products[indice]

    print("cart delete despues de borar")
    print(lists_products)

    print("request.session[lists_products] -> antes")
    print(request.session["lists_products"])
    request.session["lists_products"] = lists_products
    print("request.session[lists_products] -> despues")
    print(request.session["lists_products"])


    total = 0
    count = 0

    for item in lists_products:        # lists_products:
        total = item['subtotal'] + total
        count = item['quantity'] + count

    request.session["total_invoice"] = total
    request.session["count_products"] = count

    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        "lists": request.session["cart"],
        "lists_products": request.session["lists_products"],
        "total": request.session["total_invoice"],
        "count": request.session["count_products"]
    }
    return render(request, "cart/cart.html", context=data)
    # return HttpResponseRedirect("/cart")


def cart_save(request):
    print("cart_save")
    cart = request.session["lists_products"]
    print(cart)

    print("user")
    print(request.user.id)

    list_products = []

    for prod in cart:
        list_products.append(prod['id'])

    print(list_products)

    p = Product.objects.get(id=4)

    order = Order.objects.create(
        product=p,
        user=request.user.id
    )
    order.save()

    return HttpResponseRedirect("products/")







