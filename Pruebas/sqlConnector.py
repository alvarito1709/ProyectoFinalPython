import pyodbc
from tkinter import *
from ClassPaquete import Paquete
from ClassUser import User

#parametros para la conexion a la BBDD
parametros_conexion = (
    r'DRIVER={SQL Server};'
    #Base de datos EMILIO SERVER=DESKTOP-MM59BEH\SQLEXPRESS
    r'SERVER=DESKTOP-5QHOBD5\SQLEXPRESS;'
    r'DATABASE=DB_USUARIOS;'
    r'Trusted_Connection=yes;'
)




def validarusuario(user, pw):
	try:
		
		#utiliza los parametros declarados anteriormente para conectarse a la BBDD
		conexion = pyodbc.connect(parametros_conexion)
		print("Conexión exitosa")

		cursor = conexion.cursor()

        # Consulta para verificar usuario, contraseña y rol
		query = 'SELECT rol FROM usuarios WHERE usuario = ? AND contraseña = ?'
		cursor.execute(query, (user.get(), pw.get()))

		result = cursor.fetchone()

		if result:
			rol = result[0]
			if rol == 1:  # Si rol es True (1)
				print("Usuario Administrador")
                
				return "user_admin"
                
			else:  # Si rol es False (0)
				print("Usuario Normal")
					
				return "user_cliente"
			
		else:
		
			return "usuario no encontrado"
			
            

		cursor.close()
		conexion.close()

	except pyodbc.Error as error:
		print("Error al conectar a la base de datos:", error)
		

def usuarioNuevo(user : User):
	
	if isinstance(user, User):
	
		try:
			conexion = pyodbc.connect(parametros_conexion)
			print("Conexión exitosa")

			cursor = conexion.cursor()

			# Query para insertar nuevo usuario
			query = "INSERT INTO usuarios (usuario, contraseña, rol, email) VALUES(?,?,?,?)"
			
			try:
				
				#ejecuta la query que declaramos anteriormente
				cursor.execute(query, (user.usuario, user.contrasena, user.rol, user.email))

				conexion.commit()
				
			except pyodbc.Error as err:
				
				print("error al agregar usuario", err)
				
				

			cursor.close()
			conexion.close()

		except pyodbc.Error as error:
			print("Error al conectar a la base de datos:", error.with_traceback)
			
	else:
		print("El objeto tiene que ser de tipo User")
		
		



def paqueteNuevo(paquete : Paquete):
	
	if isinstance(paquete, Paquete):
		
		try:
			conexion = pyodbc.connect(parametros_conexion)
			print("Conexión exitosa")

			cursor = conexion.cursor()

			# Query para insertar nuevo usuario
			query = "INSERT INTO paquetes (destino, duracion, precio, stock) VALUES(?,?,?,?)"
			
			try:
					
				#ejecuta la query que declaramos anteriormente
				cursor.execute(query, (paquete.destino, paquete.duracion, paquete.precio, paquete.stock))

				conexion.commit()
					
			except pyodbc.Error as err:
					
				print("error al agregar paquete", err)
				
				

			cursor.close()
			conexion.close()

		except pyodbc.Error as error:
			print("Error al conectar a la base de datos:", error.with_traceback)
			
	else:
		print("El objeto debe ser de tipo Paquete")

		
