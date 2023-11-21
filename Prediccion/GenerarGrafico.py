from matplotlib import pyplot as plt
import time

class GenerarGrafico:
    @staticmethod
    def generar_grafico(fechas_prediccion, ventas_prediccion, indice):
        try:
            # Crear el gráfico con el backend 'Agg'
            plt.switch_backend('Agg')
            plt.figure(figsize=(12, 6))  # Ajustar tamaño del gráfico

            # Configurar etiquetas y título
            plt.xlabel('Fechas')
            plt.ylabel('Venta Estimada')

            # Rotar las etiquetas del eje X para mayor legibilidad
            plt.xticks(rotation=45)

            # Ajustar el tamaño de la fuente del título
            semana = 1 + (indice // 7)
            plt.title(f'Semana {semana}', fontsize=16)  # Ajustar tamaño de la fuente del título

            # Graficar puntos y mostrar valor al lado
            for fecha, venta in zip(fechas_prediccion, ventas_prediccion):
                plt.scatter(fecha, venta, marker='o', color='blue')
                plt.text(fecha, venta, f'{venta:.2f}', fontsize=10, va='bottom', ha='center')

            # Generar un nombre de archivo único con un timestamp e índice
            timestamp = int(time.time())
            nombre_archivo = f'static/img/grafico_{timestamp}_{indice}.png'

            # Guardar el gráfico como una imagen
            plt.tight_layout()
            plt.savefig(nombre_archivo)

            # Cerrar la figura para liberar memoria
            plt.close('all')

            return nombre_archivo  # Devolver el nombre del archivo generado
        except Exception as e:
            print(f"Error al generar el gráfico: {str(e)}")
            return None

