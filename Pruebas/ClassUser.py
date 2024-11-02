import uuid

class User:

	def __init__(self, usuario: str, contrasena: str, rol: int, email: str, id: str = None):
		
		self.id = uuid.uuid4()
		
		self.usuario = usuario
		
		self.contrasena = contrasena
		
		self.rol = 1 if rol == 1 else 2
		
		self.email = email
		


def crearUsuario(usuario, contrasena, rol, email):
	
	return User(usuario, contrasena, rol, email)
	

#usuario = crearUsuario('alvaro', '12345','ADMIN', 'alvaro@mail.com')

#print(usuario.email, usuario.usuario)
	
