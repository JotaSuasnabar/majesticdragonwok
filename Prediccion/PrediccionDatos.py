import numpy as np
from sklearn.linear_model import LinearRegression


class Prediccion:

    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    @staticmethod
    def predecir_ventas(modelo, fecha_inicio, dias_a_predecir):
        fecha_inicio = np.datetime64(fecha_inicio)
        fechas_prediccion = [fecha_inicio + np.timedelta64(i-1, 'D') for i in range(1, dias_a_predecir+1)]
        fechas_prediccion_numericas = np.array([(fecha - fecha_inicio) / np.timedelta64(1, 'D') for fecha in fechas_prediccion]).reshape(-1, 1)

        ventas_prediccion = modelo.predict(fechas_prediccion_numericas)

        return fechas_prediccion, ventas_prediccion




