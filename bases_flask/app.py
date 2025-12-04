from flask import Flask, render_template, request
from flask import make_response, jsonify
import json
import math
import bases_flask.forms as forms 
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route("/index")
def index():
    titulo = "IEVN1001"
    listado = ["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template('index.html', titulo = titulo, listado = listado)

@app.route("/aporb")
def aporb():
    return render_template('aporb.html')


@app.route("/resultado", methods = ['POST'])
def resultado():
    n1 = request.form.get("a")
    n2 = request.form.get("b")
    return "La multiplicacion de {} y {} es {}".format(n1,n2,int(n1)*int(n2))

@app.route("/distancia", methods=['POST', 'GET'])
def distancia():
    if request.method == 'POST':
        x1 = request.form.get("x1")
        y1 = request.form.get("y1")
        x2 = request.form.get("x2")
        y2 = request.form.get("y2")
        distancia = math.sqrt((int(x2) - int(x1))**2 + (int(y2) - int(y1))**2)
        return render_template("distancia.html", distancia=distancia)
    return render_template("distancia.html")

@app.route('/figuras', methods=['GET', 'POST'])
def figuras():
    area = None
    figura = None
    diametro = None

    if request.method == 'POST':
        figura = request.form['figura']
        base = request.form.get('base', type=float)
        altura = request.form.get('altura', type=float)
        radio = request.form.get('radio', type=float)
        lado = request.form.get('lado', type=float)

        if figura == 'rectangulo' and base and altura:
            area = base * altura
        elif figura == 'triangulo' and base and altura:
            area = (base * altura) / 2
        elif figura == 'circulo' and radio:
            area = math.pi * (radio**2)
        elif figura == 'pentagono' and lado and altura:
            diametro = 5 * lado
            area = (diametro * altura) / 2

    return render_template('figuras.html', area=area, figura=figura)

@app.route("/hola")
def func():
    return "<h1>Hello!</h1>"

@app.route("/alumnos",methods=['GET', 'POST'])
def alumnos():
    mat = 0
    nom = ''
    ape = ''
    email = ''
    estudiantes = []
    datos = {}
    alumno_clas = forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():

        if request.form.get("btnElimina") == 'eliminar':
            response = make_response(render_template('Alumnos.html'))
            response.delete_cookie('usuario')

        mat = alumno_clas.matricula.data
        nom = alumno_clas.nombre.data
        ape = alumno_clas.apellido.data
        email = alumno_clas.email.data

        datos = {'matricula':mat, 'nombre':nom.rstrip(),
                 'apellido':ape.rstrip(), 'email':email.rstrip()}
        data_str = request.cookies.get("usuario")
        if not data_str:
            return "No hay cookie guardada", 404
        
        estudiantes = json.loads(data_str)
        estudiantes.append(datos)
    response = make_response(render_template('Alumnos.html',
            form = alumno_clas, mat = mat, nom = nom, ape = ape, email = email))
    if request.method!='GET':
        response.set_cookie('usuario', json.dumps(estudiantes))
    
    return response

@app.route("/get_cookie")
def get_coockie():
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No coockies guardadas", 404
    estudiantes = json.loads(data_str)

    return jsonify(estudiantes)

@app.route("/distanciaForms",methods=['GET', 'POST'])
def distanciaForms():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    dist = 0
    dist_cls = forms.Distacia(request.form)
    if request.method == 'POST' and dist_cls.validate():
        x1 = dist_cls.x1.data
        y1 = dist_cls.y1.data
        x2 = dist_cls.x2.data
        y2 = dist_cls.y2.data
        dist = math.sqrt((int(x2) - int(x1))**2 + (int(y2) - int(y1))**2)
    return render_template('distanciaForm.html',
                           form = dist_cls, x1 = x1, y1 = y1, x2 = x2, y2 = y2, dist =dist)

def calcular_subtotal(tam, ing, cant):
    # Asignar el precio base según el tamaño
    if tam == 'chica':
        precio_base = 40
    elif tam == 'mediana':
        precio_base = 80
    elif tam == 'grande':
        precio_base = 120
    else:
        precio_base = 0

    # Calcular el precio total de los ingredientes
    precio_ingredientes = 0
    for i in ing:
        if i == 'jamon':
            precio_ingredientes = precio_ingredientes + 10
        elif i == 'pina':
            precio_ingredientes = precio_ingredientes + 10
        elif i == 'champi':
            precio_ingredientes = precio_ingredientes + 10

    # Calcular el subtotal total
    subtotal = (precio_base + precio_ingredientes) * cant
    return subtotal


@app.route("/pizzas", methods=['GET', 'POST'])
def pizzas():
    pizza_cls = forms.Pizzas(request.form)
    pedidos = []
    ventas = []
    total = 0
    total_dia = 0
    mensaje = ""

    # Leer cookies si existen
    data_str = request.cookies.get("pedido")
    if data_str:
        pedidos = json.loads(data_str)

    ventas_str = request.cookies.get("cookie_ventas")
    if ventas_str:
        ventas = json.loads(ventas_str)

    # BOTÓN QUITAR INDIVIDUAL
    if request.form.get("btnQuitar") == "quitar":
        index = int(request.form.get("index"))
        if index >= 0 and index < len(pedidos):
            pedidos.pop(index)

        # Calcular el total del día
        total_dia = 0
        for v in ventas:
            total_dia = total_dia + v["total"]

        response = make_response(render_template("pizzas.html",
            form=pizza_cls, pedidos=pedidos, ventas=ventas, total_dia=total_dia))
        response.set_cookie("pedido", json.dumps(pedidos))
        return response

    # BOTÓN ELIMINAR
    if request.form.get("btnElimina") == "eliminar":
        # Calcular total del día antes de limpiar
        total_dia = 0
        for v in ventas:
            total_dia = total_dia + v["total"]

        response = make_response(render_template("pizzas.html",
            form=pizza_cls, ventas=ventas, total_dia=total_dia))
        response.delete_cookie("pedido")
        return response

    # BOTÓN TERMINAR PEDIDO
    if request.form.get("btnTerminar") == "terminar":
        if len(pedidos) > 0:
            total = 0
            for p in pedidos:
                total = total + p["subtotal"]

            cliente = pedidos[0]
            venta = {
                "nombre": cliente["nombre"],
                "direccion": cliente["direccion"],
                "telefono": cliente["telefono"],
                "total": total
            }

            ventas.append(venta)

            # Calcular total del día
            total_dia = 0
            for v in ventas:
                total_dia = total_dia + v["total"]

            response = make_response(render_template("pizzas.html",
                form=pizza_cls, pedidos=[], total=total,
                mensaje="Pedido terminado correctamente", ventas=ventas, total_dia=total_dia))
            response.delete_cookie("pedido")
            response.set_cookie("cookie_ventas", json.dumps(ventas))
            return response
        else:
            mensaje = "No hay pizzas agregadas para terminar el pedido."

    # BOTÓN AGREGAR PIZZA
    if request.method == 'POST' and pizza_cls.validate():
        if request.form.get("btnAgregar") == "agregar":
            nombre = pizza_cls.nombreP.data
            direccion = pizza_cls.direccionP.data
            tel = pizza_cls.telefonoP.data
            cant = pizza_cls.numPizzasP.data
            tam = pizza_cls.tamP.data
            ing = pizza_cls.ingP.data

            subtotal = calcular_subtotal(tam, ing, cant)

            datos = {
                "nombre": nombre,
                "direccion": direccion,
                "telefono": tel,
                "cantidad": cant,
                "tamano": tam,
                "ingredientes": ", ".join(ing),
                "subtotal": subtotal
            }

            pedidos.append(datos)

            # Calcular total del día
            total_dia = 0
            for v in ventas:
                total_dia = total_dia + v["total"]

            response = make_response(render_template("pizzas.html",
                form=pizza_cls, pedidos=pedidos, ventas=ventas, total_dia=total_dia))
            response.set_cookie("pedido", json.dumps(pedidos))
            return response

    # VISTA INICIAL
    total_dia = 0
    for v in ventas:
        total_dia = total_dia + v["total"]

    return render_template("pizzas.html",
        form=pizza_cls, pedidos=pedidos, ventas=ventas, total_dia=total_dia, mensaje=mensaje)


@app.route("/get_pedido")
def get_pedido():
    data_str = request.cookies.get("pedido")
    if not data_str:
        return "No hay pedidos guardados", 404
    pedidos = json.loads(data_str)
    return jsonify(pedidos)



@app.route("/user/<string:user>")
def user(user):
    return "<h1>Hello, {}!</h1>".format(user)

@app.route("/square/<int:num>")
def square(num):
    return "<h1>The square of {} is {}</h1>".format(num, num**2)

@app.route("/repeat/<string:text>/<int:times>")
def repeat(text, times):
    return "<h1>" + " ".join([text] * times) + "</h1>"

@app.route("/suma/<float:a>/<float:b>")
def suma(a, b):
    return "<h1> The sum of {} and {} is {} </h1".format(a, b, a + b)
    
if __name__ == '__main__':
    app.run(debug=True)