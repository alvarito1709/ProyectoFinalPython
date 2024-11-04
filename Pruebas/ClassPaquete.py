import uuid

class Paquete:

	
	
	def __init__(self, destino: str, duracion: int, precio : float, stock: int, id_paquete:int = None):
		
		self.id_paquete = id_paquete 
		
		self.destino = destino
		
		self.duracion = duracion
		
		self.precio = precio
		
		self.stock = stock
	
	
def crearPaquete(destino, duracion, precio, stock):
	
	return Paquete(destino,duracion, precio, stock)
	
	
#paqueteNuevo = crearPaquete('Dubai', 5, 500, 10)

#print(paqueteNuevo.destino, paqueteNuevo.duracion, paqueteNuevo.precio, paqueteNuevo.stock)
