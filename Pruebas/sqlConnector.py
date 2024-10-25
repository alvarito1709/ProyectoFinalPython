import pyodbc
from tkinter import *



parametros_conexion = (
    r'DRIVER={SQL Server};'
    #Base de datos EMILIO SERVER=DESKTOP-MM59BEH\SQLEXPRESS
    r'SERVER=DESKTOP-5QHOBD5\SQLEXPRESS;'
    r'DATABASE=DB_USUARIOS;'
    r'Trusted_Connection=yes;'
)




def validarusuario(user, pw):
	try:
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
		

def usuarioNuevo(usuario, contrasena, rol, email):
	
	try:
		conexion = pyodbc.connect(parametros_conexion)
		print("Conexión exitosa")

		cursor = conexion.cursor()

        # Consulta para verificar usuario, contraseña y rol
		query = "INSERT INTO usuarios (usuario, contraseña, rol, email) VALUES(?,?,?,?)"
		
		try:
			cursor.execute(query, (usuario, contrasena, rol, email))

			conexion.commit()
			
		except pyodbc.Error as err:
			
			print("error al agregar usuario", err)
			
            

		cursor.close()
		conexion.close()

	except pyodbc.Error as error:
		print("Error al conectar a la base de datos:", error.with_traceback)

