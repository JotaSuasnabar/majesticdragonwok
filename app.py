from datetime import datetime, timedelta
import os
from Prediccion.conexion import Conexion
from Prediccion.ObtenerDatos import ObtenerDatos
from Prediccion.EntrenamientoDatos import EntrenamiendoDatos
from Prediccion.PrediccionDatos import Prediccion
from Prediccion.GenerarGrafico import GenerarGrafico
from flask import Flask, render_template, request, redirect, url_for
from flask import redirect
from flask import Flask
from flask_login import LoginManager
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from sklearn.linear_model import LinearRegression

app = Flask(__name__)


# Configuración de la base de datos
db = Conexion.conectar_bd('bstphlah0yvuxack5rrn-mysql.services.clever-cloud.com', 'u1a10jgnsclu57s5', 'yEUI4WtkQe0QgIvhBbhr', 'bstphlah0yvuxack5rrn')
ObtenerD = ObtenerDatos(db)
EntrenarD = EntrenamiendoDatos()
PrediccionD = Prediccion()
GenerarG = GenerarGrafico()

app.config['SECRET_KEY'] = os.urandom(24)

# Inicializar Flask-Login
login_manager = LoginManager(app)

# Definir una clase de Usuario para interactuar con Flask-Login
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username

# Función para cargar un usuario en la sesión
@login_manager.user_loader
def load_user(username):
    return Usuario(username)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    password = request.form['password']
    
    # Consultar la base de datos para verificar las credenciales
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, password))
    usuario_encontrado = cursor.fetchone()
    cursor.close()

    if usuario_encontrado:
        # Autenticación exitosa, cargar usuario en sesión
        usuario = Usuario(usuario)
        login_user(usuario)
        return redirect(url_for('dashboard'))
    else:
        # Autenticación fallida, mostrar alerta y redirigir a la página de inicio de sesión
        return render_template('login.html', error='Credenciales incorrectas. Por favor, inténtalo de nuevo.')

@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener nombre de archivos de las predicciones
    nombres_archivos = request.args.getlist('nombres_archivos')

    # Dividir la lista de nombres de archivos en dos bloques
    nombres_archivos_1 = nombres_archivos[:len(nombres_archivos)//2]
    nombres_archivos_2 = nombres_archivos[len(nombres_archivos)//2:]

    return render_template('plantilla.html', nombres_archivos_1=nombres_archivos_1, nombres_archivos_2=nombres_archivos_2)



@app.route('/logout')
@login_required
def logout():
    # Cierra la sesión del usuario
    logout_user()

    # Redirige al usuario a la página de inicio de sesión
    return redirect(url_for('index'))

''''''''''''''''''''''''''''''''''''
'''''''Registrarse'''''''
''''''''''''''''''''''''''''''''''''

@app.route('/registrarse')
def registrarse(): # Llamada a la función ver_registros sin argumentos
    return render_template('registrarse.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    rol = request.form['rol']

    # Insertar los datos en la base de datos (debes implementar esta lógica)
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, clave, nombre, apellido, rol) VALUES (%s, %s, %s, %s, %s)",
                   (usuario, password, nombre, apellido, rol))
    db.commit()
    cursor.close()

    # Después del registro, redirige a donde desees (por ejemplo, la página de inicio de sesión)
    return redirect(url_for('index'))


''''''''''''''''''''''''''''''''''''
'''''''Prediccion de Demanda'''''''
''''''''''''''''''''''''''''''''''''

@app.route('/form-detalles', methods=['POST'])
def obtener_detalles():
    Tinicio = request.form['Tinicio']
    Tfin = request.form['Tfin']
    TDatos = request.form['TDatos']
    Pinicio = request.form['Pinicio']
    Pfin = request.form['periodo']
    return redirect(url_for('generar_prediccion', Tinicio=Tinicio, Tfin=Tfin, Pinicio=Pinicio, Pfin=Pfin, TDatos=TDatos))

@app.route('/generar_prediccion')
def generar_prediccion():
    try:
        # Obtener fechas de la URL
        Tinicio = request.args.get('Tinicio')
        Tfin = request.args.get('Tfin')
        TDatos = request.args.get('TDatos')
        fecha_inicio_prediccion = request.args.get('Pinicio')
        fecha_fin_prediccion = int(request.args.get('Pfin'))
        
        # Convertir fecha_inicio_prediccion a datetime.date
        fecha_inicio_prediccion = datetime.strptime(fecha_inicio_prediccion, "%Y-%m-%d").date()

        # Calcular la diferencia en días
        dias_a_predecir = fecha_fin_prediccion

        if TDatos == "todosD":  # Si TDatos está presente (seleccionado)
            fechas_entrenamiento, ventas_entrenamiento = ObtenerD.obtener_datos_entrenamiento_completo()
        else:
            # Obtener datos de entrenamiento según las fechas especificadas
            fechas_entrenamiento, ventas_entrenamiento = ObtenerD.obtener_datos_entrenamiento(Tinicio, Tfin)
        
        # Entrenar modelo de regresión lineal
        modelo = LinearRegression()
        modelo.fit(fechas_entrenamiento.reshape(-1, 1), ventas_entrenamiento)
        
        # Inicializar listas de nombres de archivo
        nombres_archivos = []

        # Generar gráficos cada 7 días hasta alcanzar la cantidad total de días a predecir
        for i in range(0, dias_a_predecir, 7):
            fecha_inicio_bloque = fecha_inicio_prediccion + timedelta(days=i)
            fechas_prediccion, ventas_prediccion = PrediccionD.predecir_ventas(modelo, fecha_inicio_bloque, min(7, dias_a_predecir - i))
            nombre_archivo = GenerarGrafico.generar_grafico(fechas_prediccion, ventas_prediccion, i)
            nombres_archivos.append(nombre_archivo)
            print(f"Fechas predicción para el bloque {i+1}: {fechas_prediccion}")
            print(f"Ventas predicción para el bloque {i+1}: {ventas_prediccion}")

        # Pasar correctamente los nombres de archivo a la URL
        return redirect(url_for('dashboard', nombres_archivos=nombres_archivos))

    except Exception as e:
        print(f"Error en la generación de predicciones: {str(e)}")
        return redirect(url_for('dashboard', nombres_archivos=[]))




''''''''''''''''''''''''''''''''''''
'''''Segmentacion de Clientes'''''
''''''''''''''''''''''''''''''''''''
@app.route('/ver_productos')
def ver_datos_productos():
    datosP = ObtenerD.mostrar_datos_productos()  # Llamada a la función ver_registros sin argumentos
    return render_template('ver_productos.html', datosP=datosP)

if __name__ == '__main__':
    app.run(debug=True)