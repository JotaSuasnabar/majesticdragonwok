import numpy as np
from Prediccion.conexion import Conexion

class ObtenerDatos:
        
    def __init__(self, conexion):
        self.cursor = conexion.cursor()

    def ver_registros(self):
        query= "SELECT id, comida, id_orden, cantidad, p_unitario, p_total, extras, fecha FROM o_pedidos;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados
    
    
    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    
    def mostrar_datos_entrenamiento(self):
        query= "SELECT fecha, SUM(p_total) FROM o_pedidos WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY fecha;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados

    @staticmethod
    def obtener_datos_entrenamiento(fecha_inicio, fecha_fin):
        conexion = Conexion.conectar_bd('sql5.freesqldatabase.com', 'sql5664118', '7DSQiuVlZH', 'sql5664118', port=3306)
        cursor = conexion.cursor()
        consulta = "SELECT fecha, SUM(p_total) FROM o_pedidos WHERE fecha BETWEEN %s AND %s GROUP BY fecha"
        cursor.execute(consulta, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        fechas, ventas = zip(*resultados)
        fechas = np.array([np.datetime64(fecha) for fecha in fechas]).reshape(-1, 1)
        ventas = np.array(ventas)
        return fechas, ventas

    @staticmethod
    def obtener_datos_entrenamiento_completo():
        conexion = Conexion.conectar_bd('sql5.freesqldatabase.com', 'sql5664118', '7DSQiuVlZH', 'sql5664118', port=3306)
        cursor = conexion.cursor()
        consulta = "SELECT fecha, SUM(p_total) FROM o_pedidos GROUP BY fecha"
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        fechas, ventas = zip(*resultados)
        fechas = np.array([np.datetime64(fecha) for fecha in fechas]).reshape(-1, 1)
        ventas = np.array(ventas)
        return fechas, ventas

    
    ''''''''''''''''''''''''''''''''''''
    '''''''Segmentacion de Clientes'''''''
    ''''''''''''''''''''''''''''''''''''
    def mostrar_datos_productos(self):
        query= """SELECT fecha, comida, SUM(cantidad) as Cantidad_total, DAYOFWEEK(fecha) as Dia_semana FROM o_pedidos WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY comida, fecha"""
        #query = "SELECT comida, fecha, SUM(cantidad) as total_cantidad FROM o_pedidos GROUP BY comida, fecha;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados