# GRUPO 10: Cifuentes Juan, Ortiz Alvaro, Maidana Emilio
# DIA Y HORARIO: 12/11 - 20:40 HS
# Crear un programa para el manejo de viajes de una empresa de turismo teniendo en cuenta
# los siguientes aspectos:

# 1) El sistema debe ser de acceso restringido sólo para algunas opciones especiales (a
# considerar según el grupo de trabajo)
# 2) Planificación de viajes, destinos, duración y precios de los mismos
# 3) Salida de comprobantes por pantalla.

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import List, Any

import pyodbc

import sqlConnector as sql
from ClassPaquete import Paquete, crearPaquete

from ClassUser import User


#conecto a la base de datos


#paquetenuevo = Paquete('Bariloche',5, 124300.50, 10)
#sql.paqueteNuevo(paquetenuevo)


def ventana_user(lienzo):
	
	lienzo.destroy()
    
	lienzo = tk.Tk()
    
	lienzo.geometry("800x400")
    
	lienzo.title("User")
	
	lienzo.iconbitmap("viajes.ico")
    
    #recuadro destino
	groupbox = LabelFrame(lienzo, text="Seleccione el destino", padx=5, pady=5)
    
	groupbox.grid(row=1, column=0, padx=0, pady=0)
    
	labelDest = Label(groupbox, text="Destino ", width=13, font=("Arial", 12)).grid(row=1, column=0)
    
	labeldestino = Label(groupbox, text="Seleccione el destino: ", width=20, font=("Arial", 12)).grid(row=1,column=0)
    
	select_destino = tk.StringVar()
    
	listaPaquetes = {}
    
	destinosSQL = sql.listarPaquetes()
    
	for i in destinosSQL:
		listaPaquetes[i.destino] = i.id_paquete
		
	nombrePaquetes = list(listaPaquetes.keys())
    
	combo = ttk.Combobox(lienzo, values= nombrePaquetes,width=30, textvariable=select_destino)
	combo.grid(row=1, column=1)
	
	
	def buscarPaqueteSeleccionado(event):
		
		destino = combo.get()
		
		destinoConId = listaPaquetes[destino]
		
		infoPaquete = sql.buscarPaquetePorId(destinoConId)
		
		print("El paquete seleccionado viaja a: \n", infoPaquete.destino, "\n Y tiene un coste de: \n", infoPaquete.precio)
		
		return infoPaquete
		
	combo.bind("<<ComboboxSelected>>", lambda event: buscarPaqueteSeleccionado(event))
	
	lienzo.mainloop()
    
	return



def modificar_paquete(tree, paquetes):
	seleccion = tree.selection()[0]  # Obtener la fila seleccionada
	if seleccion:
		item = tree.item(seleccion)
		
		valores = item['values']  # Obtener los demás valores
		id_paquete = valores[0]  # Obtener ID del paquete

		ventana_mod = tk.Toplevel()
		ventana_mod.title("Modificar Paquete")
		ventana_mod.geometry("400x600")


		# Crear etiquetas y entradas para cada parámetro
		tk.Label(ventana_mod, text="ID Paquete").pack(pady=5)
		label_id = tk.Label(ventana_mod, text=id_paquete, relief="sunken")
		label_id.pack(pady=5)

		tk.Label(ventana_mod, text="Destino").pack(pady=5)
		entry_destino = ttk.Entry(ventana_mod)
		entry_destino.insert(0, valores[1])  # Precargar valor
		entry_destino.pack(pady=5)

		tk.Label(ventana_mod, text="Duración").pack(pady=5)
		entry_duracion = ttk.Entry(ventana_mod)
		entry_duracion.insert(0, valores[2])  # Precargar valor
		entry_duracion.pack(pady=5)

		tk.Label(ventana_mod, text="Precio").pack(pady=5)
		entry_precio = ttk.Entry(ventana_mod)
		entry_precio.insert(0, valores[3])  # Precargar valor
		entry_precio.pack(pady=5)

		tk.Label(ventana_mod, text="Stock").pack(pady=5)
		entry_stock = ttk.Entry(ventana_mod)
		entry_stock.insert(0, valores[4])  # Precargar valor
		entry_stock.pack(pady=5)
		
		
		
		#ver porque no sale el boton(solucionado)
		boton = tk.Button(ventana_mod, text="Modificar paquete",
						  command=lambda: guardarcambios())
		boton.pack(pady=10)
		
		#ver porque no puede guardar los datos en la base de datos
		def guardarcambios():
			
			try:
				
				destino = entry_destino.get()
				duracion = int(entry_duracion.get())
				precio = float(entry_precio.get())
				stock = int(entry_stock.get())
				idPack = int(id_paquete)

				pack = Paquete(destino, duracion, precio, stock, idPack)
	

				sql.modificarPaquete(pack)
				
			except ValueError as error:
				
				messagebox.showerror({error}, 'Por favor ingrese valores validos')
				
			except Exception as exc: 
				
				messagebox.showerror('Error al guardar los cambios ',{exc})
				
			
			# Actualizar el Treeview
			paquetes = sql.listarPaquetes()
			
			for item in tree.get_children():
				
				tree.delete(item)

			for paquete in paquetes:
				tree.insert('', 'end', values=(paquete. id_paquete, paquete.destino, paquete.duracion, paquete.precio, paquete.stock, paquete.stock))
			ventana_mod.destroy()  # Cerrar la ventana de modificación




def ventana_modpaq(lienzo):
	lienzo.destroy()
	lienzo = tk.Tk()
	lienzo.geometry("1000x600")
	lienzo.pack_propagate(False)
	lienzo.resizable(True, True)
	lienzo.title("Modificar paquete")
	#crea el treeview
	tree = ttk.Treeview(lienzo, columns=('id_paquete','Destino', 'Duracion', 'Precio', 'Stock'), show='headings')
	tree.heading('id_paquete', text='id_paquete')
	tree.heading('Destino', text='Destino')
	tree.heading('Duracion', text='Duracion')
	tree.heading('Precio', text='Precio')
	tree.heading('Stock', text='Stock')

	tree.pack(side='top', fill='both', expand=True)

	# Crear una barra de desplazamiento
	scrollbar = ttk.Scrollbar(lienzo, orient='vertical', command=tree.yview)
	tree.configure(yscroll=scrollbar.set)
	scrollbar.pack(side='right', fill='y')



	paquetes = sql.listarPaquetes()

	for paquete in paquetes:
		tree.insert('', 'end', values=(paquete.id_paquete, paquete.destino, paquete.duracion, paquete.precio, paquete.stock, paquete.stock))

	# Crear un botón que actúa sobre la fila seleccionada
	boton = tk.Button(lienzo, text="Modificar paquete", command=lambda: modificar_paquete(tree,paquetes))
	boton.pack(pady=10)

	lienzo.mainloop()

def ventana_addpaq(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x300")
    lienzo.title("Agregar Paquete")


    # Etiquetas y entradas para los datos del nuevo paquete
    tk.Label(lienzo, text="Destino").grid(row=0, column=0, padx=10, pady=10)
    entry_destino = tk.Entry(lienzo, width=30)
    entry_destino.grid(row=0, column=1, padx=10, pady=10)


    tk.Label(lienzo, text="Duración (días)").grid(row=1, column=0, padx=10, pady=10)
    entry_duracion = tk.Entry(lienzo, width=30)
    entry_duracion.grid(row=1, column=1, padx=10, pady=10)


    tk.Label(lienzo, text="Precio").grid(row=2, column=0, padx=10, pady=10)
    entry_precio = tk.Entry(lienzo, width=30)
    entry_precio.grid(row=2, column=1, padx=10, pady=10)


    tk.Label(lienzo, text="Stock").grid(row=3, column=0, padx=10, pady=10)
    entry_stock = tk.Entry(lienzo, width=30)
    entry_stock.grid(row=3, column=1, padx=10, pady=10)


    # Función para agregar paquete
    def agregar_paquete():
        destino = entry_destino.get()
        duracion = int(entry_duracion.get())
        precio = float(entry_precio.get())
        stock = int(entry_stock.get())


        nuevo_paquete = Paquete(destino, duracion, precio, stock)
       
        # Llama a la función en sqlConnector para agregar el paquete
        sql.paqueteNuevo(nuevo_paquete)
        messagebox.showinfo("Éxito", f"Paquete a {destino} agregado exitosamente.")
        lienzo.destroy()


    # Botón para agregar el paquete
    boton_agregar = tk.Button(lienzo, text="Agregar Paquete", command=agregar_paquete)
    boton_agregar.grid(row=4, column=0, columnspan=2, pady=20)


    lienzo.mainloop()

def ventana_delpaq(lienzo):
	lienzo.destroy()
	lienzo = tk.Tk()
	lienzo.geometry("550x400")
	lienzo.title("Eliminar paquete")

	# Treeview para mostrar paquetes
	tree = ttk.Treeview(lienzo, columns=('id_paquete', 'Destino', 'Duracion', 'Precio', 'Stock'), show='headings')
	tree.heading('id_paquete', text='ID Paquete')
	tree.heading('Destino', text='Destino')
	tree.heading('Duracion', text='Duración')
	tree.heading('Precio', text='Precio')
	tree.heading('Stock', text='Stock')
	tree.pack(side='top', fill='both', expand=True)

	# Rellenar el Treeview con los paquetes de la base de datos
	paquetes = sql.listarPaquetes()
	for paquete in paquetes:
		tree.insert('', 'end',
					values=(paquete.id_paquete, paquete.destino, paquete.duracion, paquete.precio, paquete.stock))

	# Función para manejar la eliminación
	def eliminar_paquete_seleccionado():
		seleccion = tree.selection()
		if seleccion:
			item = tree.item(seleccion)
			paquete_id = item['values'][0]

			# Confirmación
			if messagebox.askyesno("Confirmación", f"¿Está seguro de eliminar el paquete ID {paquete_id}?"):
				sql.eliminarPaquete(paquete_id)
				tree.delete(seleccion)  # Eliminar del Treeview

	# Botón para eliminar el paquete seleccionado
	boton = tk.Button(lienzo, text="Eliminar paquete seleccionado", command=eliminar_paquete_seleccionado)
	boton.pack(pady=10)

	lienzo.mainloop()


def ventana_adm(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x200")
    lienzo.title("Administrador")
    
    lienzo.iconbitmap("viajes.ico")
    groupbox = LabelFrame(lienzo, text="Seleccione una opcion", padx=50, pady=5)
    groupbox.grid(row=1, column=0, padx=0, pady=0)

    Button(groupbox, text="Editar Paquete",command=lambda: ventana_modpaq(lienzo), width=20).grid(row=1, column=0)
    Button(groupbox, text="Agregar Paquete",command=lambda: ventana_addpaq(lienzo), width=20).grid(row=1, column=1)
    Button(groupbox, text="Eliminar Paquete",command=lambda: ventana_delpaq(lienzo), width=20).grid(row=1, column=2)
    Button(groupbox, text="Agregar Usuario", command=lambda: ventana_adduser(lienzo), width=20).grid(row=3, column=0)



    
def checkLogin(lienzo, username, password):
	
	usuario = sql.validarusuario(username, password)
	
	if usuario == "user_admin":
		
		ventana_adm(lienzo)
		
	elif usuario == "user_cliente":
		
		ventana_user(lienzo)
		
	else:
		messagebox.showerror("Error", "Usuario o contraseña incorrectos")


class LoginUsuario:
	def login():
		try:
			lienzo = Tk()
			lienzo.geometry("800x400")
			lienzo.title("Login")
			
			lienzo.iconbitmap("viajes.ico")

            # recuadro de Login
            # recuadro de Login
			groupbox = LabelFrame(lienzo, text="Login", padx=5, pady=5)
			groupbox.grid(column=0, row=0, padx=220, pady=20)

            # Variables para almacenar el contenido de los Entry
			username = StringVar()
			password = StringVar()

			labelname = Label(groupbox, text="Username: ", width=13, font=("Arial", 12))
			labelname.grid(row=0, column=0)
			textboxusername = Entry(groupbox, textvariable=username)
			textboxusername.grid(row=0, column=2)

			labelpw = Label(groupbox, text="Password: ", width=13, font=("Arial", 12))
			labelpw.grid(row=1, column=0)
			textboxpw = Entry(groupbox, textvariable=password, show='*')  # 'show' para ocultar la contraseña
			textboxpw.grid(row=1, column=2)

			Button(groupbox, text="Login", command=lambda: checkLogin(lienzo, username, password), width=10).grid(row=2, column=1)
            
					

            # recuadro de paquetes

			lienzo.mainloop()


		except ValueError as error:
			print("Error al mostrar la interfaz, error: {}".format(error))

	login()

def ventana_adduser(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x400")
    lienzo.title("Agregar Usuario")
   
    # Crear etiquetas y campos de entrada
    tk.Label(lienzo, text="Nombre de Usuario").pack(pady=5)
    entry_usuario = ttk.Entry(lienzo)
    entry_usuario.pack(pady=5)


    tk.Label(lienzo, text="Contraseña").pack(pady=5)
    entry_contrasena = ttk.Entry(lienzo, show='*')
    entry_contrasena.pack(pady=5)


    tk.Label(lienzo, text="Email").pack(pady=5)
    entry_email = ttk.Entry(lienzo)
    entry_email.pack(pady=5)


    tk.Label(lienzo, text="Rol (1 para admin, 0 para cliente)").pack(pady=5)
    entry_rol = ttk.Entry(lienzo)
    entry_rol.pack(pady=5)


    # Función para enviar datos al conector SQL
    def agregar_usuario():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        email = entry_email.get()
        rol = int(entry_rol.get())
       
        # Llamada a la función de sqlConnector para crear un usuario
        nuevo_usuario = User(usuario, contrasena, rol, email)
        sql.usuarioNuevo(nuevo_usuario)
        messagebox.showinfo("Éxito", f"Usuario {usuario} agregado con éxito")
        lienzo.destroy()


    # Botón para agregar usuario
    tk.Button(lienzo, text="Agregar Usuario", command=agregar_usuario).pack(pady=10)
    lienzo.mainloop()