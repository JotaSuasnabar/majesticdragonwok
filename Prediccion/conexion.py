import mysql.connector

class Conexion:
    @staticmethod
    def conectar_bd(host, usuario, contraseña, base_de_datos):
        try:
            conexion = mysql.connector.connect(
                host=host,
                user=usuario,
                password=contraseña,
                database=base_de_datos
            )
            if conexion.is_connected():
                print(f'Conexión a la base de datos {base_de_datos} exitosa')
                return conexion
        except mysql.connector.Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            if conexion and conexion.is_connected():
                conexion.close()
            return None
