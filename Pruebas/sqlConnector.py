import pyodbc
from tkinter import *
from ClassPaquete import Paquete
from ClassUser import User

#parametros para la conexion a la BBDD
parametros_conexion = (
    r'DRIVER={SQL Server};'
    #Base de datos EMILIO SERVER=DESKTOP-MM59BEH\SQLEXPRESS DESKTOP-MM59BEH\SQLEXPRESS
	
	#Base de datos JUANk 
	#r'SERVER=DESKTOP-T6Q6QH5\SQLEXPRESS;'
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
		

def listarUsuarios():
    try:
        conexion = pyodbc.connect(parametros_conexion)

        cursor = conexion.cursor()
        
        query = "SELECT id, usuario, contraseña, rol, email FROM usuarios"  # Ajusta el nombre de la tabla si es necesario
        cursor.execute(query)

        listaUsuarios = []

        # Mapeo de resultados a objetos User
        for index in cursor:
            usuario = User(index.usuario, index.contraseña, index.rol, index.email)
            usuario.id = index.id  # Usamos el ID de la base de datos
            listaUsuarios.append(usuario)

        return listaUsuarios

    except pyodbc.Error as err:
        print("Error al hacer la consulta", err)


def usuarioNuevo(user : User):
	
	if isinstance(user, User):
	
		try:
			conexion = pyodbc.connect(parametros_conexion)

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



def modificarUsuario(user: User):
    try:
        conexion = pyodbc.connect(parametros_conexion)
        cursor = conexion.cursor()

        # Consulta SQL para actualizar el usuario
        query = """UPDATE usuarios 
                   SET usuario = ?, contraseña = ?, rol = ?, email = ? 
                   WHERE id = ?"""
        cursor.execute(query, (user.usuario, user.contrasena, user.rol, user.email, user.id))
        conexion.commit()

    except pyodbc.Error as error:
        print("Error al modificar el usuario en la base de datos:", error)
    finally:
        conexion.close()		
		
#Funcion para listar todos los paquetes en la base de datos (RETORNA LISTA DE OBJETOS PAQUETE)


def eliminarUsuario(usuario_id):
    try:
        conexion = pyodbc.connect(parametros_conexion)
        cursor = conexion.cursor()

        query = "DELETE FROM usuarios WHERE id = ?"
        cursor.execute(query, usuario_id)
        conexion.commit()

        print(f"Usuario con ID {usuario_id} eliminado correctamente.")
        
    except pyodbc.Error as err:
        print("Error al intentar eliminar el usuario:", err)

    finally:
        cursor.close()
        conexion.close()




def listarPaquetes():

	try:
		conexion = pyodbc.connect(parametros_conexion)

		cursor = conexion.cursor()

		query = "SELECT * FROM paquetes"

		cursor.execute(query)

		listaPaquetes = []


		#Mapea el objeto cursor que hizo la consulta para convertir el retorno en un objeto de tipo Paquetre
		for index in cursor:

			paquete = Paquete( index.destino, index.duracion, index.precio, index.stock, index.id_paquete)

			listaPaquetes.append(paquete)

		return listaPaquetes

	except pyodbc.Error as err:

		print("Error al hacer la consulta", err)
		
		
		
#lista = listarPaquetes()

#for index in range(0,len(lista)):
	
#	print(lista[index].destino)
		


def buscarPaquetePorId(paqueteId):
	
	try:
			conexion = pyodbc.connect(parametros_conexion)

			cursor = conexion.cursor()

			# Query para buscar paquete por ID
			query = "SELECT * FROM paquetes WHERE id_paquete = ?"
			
			try:
					
				#ejecuta la query que declaramos anteriormente junto a la variable que toma por parametro la funcion
				cursor.execute(query, paqueteId)

				paquete = cursor.fetchone()
				
				return paquete
					
			except pyodbc.Error as err:
					
				print("Paquete no encontrado", err)
				
				

			cursor.close()
			conexion.close()

	except pyodbc.Error as error:
		print("Error al conectar a la base de datos:", error.with_traceback)
			
			
#buscarPaquete = buscarPaquetePorId(2)

#print(buscarPaquete.destino)


def paqueteNuevo(paquete : Paquete):
	
	
	#Verifica que la instancia sea del tipo correcto
	if isinstance(paquete, Paquete):
		
		try:
			conexion = pyodbc.connect(parametros_conexion)

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



def modificarPaquete(paquete : Paquete):

	#Verifica que la instancia sea del tipo correcto
	if isinstance(paquete, Paquete):
		
		print('paquete: ', paquete.destino, 'duracion: ', paquete.duracion, 'precio: ', 'id: ', paquete.id_paquete)

		try:
			conexion = pyodbc.connect(parametros_conexion)

			cursor = conexion.cursor()

			# Query para insertar nuevo usuario
			query = "UPDATE paquetes SET destino = ?, duracion = ?, precio = ?, stock = ? WHERE id_paquete = ?"

			try:

				#ejecuta la query que declaramos anteriormente
				cursor.execute(query, (paquete.destino, paquete.duracion, paquete.precio, paquete.stock, paquete.id_paquete))

				conexion.commit()

			except pyodbc.Error as err:

				print("error al editar paquete", err)



			cursor.close()
			conexion.close()

		except pyodbc.Error as error:
			print("Error al conectar a la base de datos:", error.with_traceback)

	else:
		print("El objeto debe ser de tipo Paquete")


def eliminarPaquete(paqueteId):
    try:
        conexion = pyodbc.connect(parametros_conexion)
        cursor = conexion.cursor()


        query = "DELETE FROM paquetes WHERE id_paquete = ?"
        cursor.execute(query, (paqueteId,))
        conexion.commit()
        cursor.close()
        conexion.close()
        print(f"Paquete con ID {paqueteId} eliminado correctamente.")
    except pyodbc.Error as err:
        print("Error al eliminar el paquete:", err)



#paqueteNuevo = Paquete('paqueteMod', 1, 1,9, 3)

#modificarPaquete(paqueteNuevo);

	
