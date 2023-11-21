import collections
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from Prediccion.ObtenerDatos import ObtenerDatos


class EntrenamiendoDatos:

    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    @staticmethod
    def entrenar_modelo(fechas, ventas):
        poly = PolynomialFeatures(degree=2)  # Usar regresión lineal (grado 1)
        fechas_poly = poly.fit_transform(fechas)
        modelo = LinearRegression()
        modelo.fit(fechas_poly, ventas)
        return modelo, poly

    ''''''''''''''''''''''''''''''''''''
    '''''''Segmentacion de Clientes'''''''
    ''''''''''''''''''''''''''''''''''''

    @staticmethod
    def entrenar_modelo_datos():
                # Obtener los datos
        (ObtenerDatos.fechas_dias_semana, ObtenerDatos.ventas_dias_semana, ObtenerDatos.productos_dias_semana, 
        ObtenerDatos.fechas_fines_semana, ObtenerDatos.ventas_fines_semana, ObtenerDatos.productos_fines_semana) = ObtenerDatos.Obtener_datos_por_dia_semana()

                # Concatenar productos y ventas para días de semana y fines de semana
        productos_ventas_dias_semana = list(zip(ObtenerDatos.productos_dias_semana, ObtenerDatos.ventas_dias_semana))
        productos_ventas_fines_semana = list(zip(ObtenerDatos.productos_fines_semana, ObtenerDatos.ventas_fines_semana))

                # Contar la cantidad de ventas por producto
        conteo_dias_semana = collections.defaultdict(int)
        conteo_fines_semana = collections.defaultdict(int)

        for producto, ventas in productos_ventas_dias_semana:
                    conteo_dias_semana[producto] += int(ventas)

        for producto, ventas in productos_ventas_fines_semana:
                    conteo_fines_semana[producto] += int(ventas)

                # Encontrar los 5 productos más vendidos
        top_productos_dias_semana = dict(sorted(conteo_dias_semana.items(), key=lambda item: item[1], reverse=True)[:5])
        top_productos_fines_semana = dict(sorted(conteo_fines_semana.items(), key=lambda item: item[1], reverse=True)[:5])

        return top_productos_dias_semana, top_productos_fines_semana

'''
# Llamando a la función para entrenar el modelo
top_productos_dias, top_productos_fines = EntrenamiendoDatos.entrenar_modelo_datos()

# Imprimiendo los resultados
print("Los 5 productos más vendidos durante los días de semana:")
for producto, ventas in top_productos_dias.items():
    print(f"Producto: {producto}, Ventas: {ventas}")

print("\nLos 5 productos más vendidos durante los fines de semana:")
for producto, ventas in top_productos_fines.items():
    print(f"Producto: {producto}, Ventas: {ventas}")
'''