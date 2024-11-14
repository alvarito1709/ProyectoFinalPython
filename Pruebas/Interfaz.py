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
import re
from tkinter import messagebox

import pyodbc

import sqlConnector as sql
from ClassPaquete import Paquete, crearPaquete

from ClassUser import User

from tkcalendar import DateEntry

from datetime import datetime

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from tkinter import Label, LabelFrame, ttk
from PIL import Image, ImageTk


def ventana_user(lienzo, idUsuario):
	
	lienzo.destroy()
    
	lienzo = tk.Tk()
    
	lienzo.geometry("400x400")
    
	lienzo.title("User")

	try:
		imagen = Image.open(r"imagen_agencia.jpg")
		imagen = imagen.resize((100, 100), Image.LANCZOS)  # Reemplaza ANTIALIAS por LANCZOS
		imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Crear un widget Label para mostrar la imagen
		label_imagen = Label(lienzo, image=imagen_tk)
		label_imagen.image = imagen_tk  # Necesario para mantener la referencia a la imagen
		label_imagen.pack(pady=10)

	except Exception as e:
		print(f"Error al cargar la imagen: {e}")	


    #recuadro destino
	groupbox = LabelFrame(lienzo, text="Seleccione el destino", padx=5, pady=5)
    
	groupbox.pack(pady = 10)
    
	
    
	labeldestino = Label(groupbox, text="Seleccione el destino: ", width=20, font=("Arial", 12)).pack(pady = 10)
    
	select_destino = tk.StringVar()
    
	listaPaquetes = {}
    
	destinosSQL = sql.listarPaquetes()
    
	for i in destinosSQL:
		if i.stock:
			listaPaquetes[i.destino] = i.id_paquete
		
	nombrePaquetes = list(listaPaquetes.keys())
    
	combo = ttk.Combobox(lienzo, values= nombrePaquetes,width=30, textvariable=select_destino)
	combo.pack(pady = 10)
	
	
	
	def crearVentanaInfo(infoPaquete,lienzo):
		lienzo.destroy()
		lienzo = tk.Tk()
		lienzo.geometry("1000x400")
		lienzo.pack_propagate(False)
		lienzo.resizable(True, True)
		lienzo.title("Comprar Paquete")
		#crea el treeview
		tree = ttk.Treeview(lienzo, columns=('Destino', 'Duracion', 'Precio', 'Stock'), show='headings')
		tree.heading('Destino', text='Destino')
		tree.heading('Duracion', text='Duracion (Dias)')
		tree.heading('Precio', text='Precio ($)')
		tree.heading('Stock', text='Stock')

		tree.pack(side='top', fill='both', expand=True)

		# Crear una barra de desplazamiento
		scrollbar = ttk.Scrollbar(lienzo, orient='vertical', command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.pack(side='right', fill='y')
		
		def compraExitosa(lienzo, idUsuario):
			
			try:
				
				datoFecha = fechaEntry.get_date()
				
				fechaFormateada = datoFecha.isoformat()
			
				sql.compraDeUsuario(idUsuario,infoPaquete.id_paquete, fechaFormateada)
				
				messagebox.showinfo("Éxito", f"Paquete a {infoPaquete.destino} comprado exitosamente.")
                        
				# Generar y abrir el PDF automáticamente
				generar_pdf(infoPaquete, idUsuario, fechaFormateada)

				ventana_user(lienzo, idUsuario)
				
			except pyodbc.Error as error:
				
				messagebox.showerror("Error", f"Debe seleccionar una fecha.{error}")
                        
		def generar_pdf(infoPaquete, idUsuario, fecha):
			# Generar el PDF y guardarlo con un nombre específico
			archivo_pdf = "compra_paquete.pdf"
			
			# Creación del PDF
			c = canvas.Canvas(archivo_pdf, pagesize=letter)
			c.drawString(100, 750, "Resumen de Compra de Paquete")
			c.drawString(100, 700, f"Usuario ID: {idUsuario}")
			c.drawString(100, 675, f"Destino: {infoPaquete.destino}")
			c.drawString(100, 650, f"Duración: {infoPaquete.duracion} días")
			c.drawString(100, 625, f"Precio: ${infoPaquete.precio}")
			c.drawString(100, 600, f"Fecha de Salida: {fecha}")
			c.save()
			
			# Abre el PDF automáticamente en el visor predeterminado de Windows
			os.startfile(archivo_pdf)

		
		
		tree.insert('', 'end', values=(infoPaquete.destino, infoPaquete.duracion, infoPaquete.precio, infoPaquete.stock,))
		
		fechaEntry = DateEntry(lienzo, width=12, background = 'darkblue', foreground = 'white', borderwidth= 2, date_pattern='y-mm-dd')
		fechaEntry.pack(padx=10, pady=10)
		
		boton = tk.Button(lienzo, text="Comprar", command=lambda: compraExitosa(lienzo,idUsuario))
		boton.pack(pady = 10)
		
		
		botonMenu = tk.Button(lienzo, text= "Menú", command = lambda: ventana_user(lienzo,idUsuario))
		botonMenu.pack(pady = 10)
		
	botonListarViajesPendientes = tk.Button(lienzo, text="Ver viajes pendientes", command = lambda: ventana_Ver_viajes_Pendientes(lienzo, idUsuario))
	
	botonListarViajesPendientes.pack(pady=10)
		
	botonSalir = tk.Button(lienzo, text="Salir", command = lambda : salirAlLogin(lienzo))
	botonSalir.pack(pady=10)
	
	
	
	
		
	
	
	def buscarPaqueteSeleccionado(event):
		
		destino = combo.get()
		
		destinoConId = listaPaquetes[destino]
		
		infoPaquete = sql.buscarPaquetePorId(destinoConId)
		
		print("El paquete seleccionado viaja a: \n", infoPaquete.destino, "\n Y tiene un coste de: \n", infoPaquete.precio)
		
		crearVentanaInfo(infoPaquete,lienzo)
		
	combo.bind("<<ComboboxSelected>>", lambda event: buscarPaqueteSeleccionado(event))
	
	lienzo.mainloop()
    
	return


def ventana_Ver_viajes_Pendientes(lienzo, idUsuario):
	
	lienzo.destroy()
	
	lienzo = tk.Tk()
	
	lienzo.geometry("1000x400")
	
	lienzo.pack_propagate(False)
	
	lienzo.resizable(True, True)
	
	lienzo.title("Tus viajes pendientes")
	
	tree = ttk.Treeview(lienzo, columns=('Destino', 'Duracion', 'Fecha de Salida'), show='headings')
	
	tree.heading('Destino', text='Destino')
	
	tree.heading('Duracion', text='Duracion (Días)')
	
	tree.heading('Fecha de Salida', text='Fecha de salida')
	
	tree.pack(side='top', fill='both', expand=True)
	
	viajes = sql.listarViajesPendientes(idUsuario)
	
	paquetes = []
	
	for i in viajes: 
		
		paquetePendiente = sql.buscarPaquetePorId(i[2])
		
		paquetes.append(paquetePendiente)
	
	
	for indice, paquete in enumerate(paquetes):
		
		tree.insert('', 'end', values=(paquete.destino, paquete.duracion, viajes[indice].fecha_salida))
		
	botonMenu = tk.Button(lienzo, text= "Menú", command = lambda: ventana_user(lienzo,idUsuario))
	
	botonMenu.pack(pady=10)
	
	
	
	



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
			
			destino = entry_destino.get()
			duracion = entry_duracion.get()
			precio = entry_precio.get()
			stock = entry_stock.get()
			idPack = int(id_paquete)
    
			if not destino or not duracion or not precio or not stock:
				messagebox.showerror("Error", "Todos los campos deben estar completos.")
				ventana_mod.destroy()
				return
    
			try:
				duracion = int(duracion)
				precio = float(precio)
				stock = int(stock)

				if duracion < 0 or precio < 0 or stock < 0:
					messagebox.showerror("Error", "Duración, Precio y Stock no pueden ser negativos.")
					ventana_mod.destroy()
					return
				
         

			except ValueError:
				messagebox.showerror("Error", "Duración y Stock deben ser números enteros, y Precio debe ser un número decimal.")
				ventana_mod.destroy()
				return
    
			pack = Paquete(destino, duracion, precio, stock, idPack)
			sql.modificarPaquete(pack)
			ventana_mod.destroy()  # Cerrar la ventana de modificación

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
	
	boton = tk.Button(lienzo, text="Menú", command=lambda: ventana_adm(lienzo))
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
		duracion = entry_duracion.get()
		precio = entry_precio.get()
		stock = entry_stock.get()
		
		# Validar campos vacíos
		if not destino or not duracion or not precio or not stock:
			messagebox.showerror("Error", "Todos los campos deben estar completos.")
			return
		
		try:
			duracion = int(duracion)
			precio = float(precio)
			stock = int(stock)

			if duracion < 0 or precio < 0 or stock < 0:
				messagebox.showerror("Error", "Duración, Precio y Stock no pueden ser negativos.")
				return


		except ValueError:
			messagebox.showerror("Error", "Duración y Stock deben ser números enteros, y Precio debe ser un número decimal.")
			return
		
		nuevo_paquete = Paquete(destino, duracion, precio, stock)
		sql.paqueteNuevo(nuevo_paquete)
		messagebox.showinfo("Éxito", f"Paquete a {destino} agregado exitosamente.")
		ventana_adm(lienzo)


    # Botón para agregar el paquete
	boton_agregar = tk.Button(lienzo, text="Agregar Paquete", command=agregar_paquete)
	boton_agregar.grid(row=4, column=0, columnspan=2, pady=20)
    
    
	boton = tk.Button(lienzo, text="Menú", command = lambda: ventana_adm(lienzo))
	boton.grid(row=4, column=2, columnspan=2, pady=20)


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
	
	boton = tk.Button(lienzo, text="Menú", command=lambda: ventana_adm(lienzo))
	boton.pack(pady=10)

	lienzo.mainloop()


def ventana_adm(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x300")
    lienzo.title("Administrador")
    
    # Intentar cargar y mostrar la imagen
    try:
        imagen = Image.open(r"imagen_agencia.jpg")
        imagen = imagen.resize((100, 100), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Crear un widget Label para mostrar la imagen y colocarlo en la ventana
        label_imagen = Label(lienzo, image=imagen_tk)
        label_imagen.image = imagen_tk  # Mantener referencia a la imagen
        label_imagen.grid(row=0, column=0, pady=10)  # Usar grid en lugar de pack

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        
	
    groupbox = LabelFrame(lienzo, text="Seleccione una opcion", padx=50, pady=5)
    groupbox.grid(row=1, column=0, padx=0, pady=0)

    Button(groupbox, text="Editar Paquete",command=lambda: ventana_modpaq(lienzo), width=20).grid(row=1, column=0)
    Button(groupbox, text="Agregar Paquete",command=lambda: ventana_addpaq(lienzo), width=20).grid(row=1, column=1)
    Button(groupbox, text="Eliminar Paquete",command=lambda: ventana_delpaq(lienzo), width=20).grid(row=1, column=2)
    
    
    Button(groupbox, text="Editar Usuario", command=lambda: ventana_moduser(lienzo), width=20).grid(row=4, column=0)
    Button(groupbox, text="Agregar Usuario", command=lambda: ventana_adduser(lienzo), width=20).grid(row=4, column=1)
    Button(groupbox, text="Eliminar Usuario", command=lambda: ventana_deluser(lienzo), width=20).grid(row=4, column=2)
    
    botonSalir = tk.Button(lienzo, text="Salir", command = lambda : salirAlLogin(lienzo))
    botonSalir.grid( pady=10)


def modificar_usuario(tree):
	
    try:
        seleccion = tree.selection()[0]  # Obtener la fila seleccionada
    
    except: 
        messagebox.showerror("error", "Debe seleccionar un usuario")
		
    if seleccion:
        item = tree.item(seleccion)
        valores = item['values']  # Obtener los valores del usuario seleccionado
        usuario_id = valores[0]  # ID del usuario

        ventana_mod = tk.Toplevel()
        ventana_mod.title("Modificar Usuario")
        ventana_mod.geometry("400x400")

        # Crear etiquetas y entradas para cada campo del usuario
        tk.Label(ventana_mod, text="ID Usuario").pack(pady=5)
        label_id = tk.Label(ventana_mod, text=usuario_id, relief="sunken")
        label_id.pack(pady=5)

        tk.Label(ventana_mod, text="Nombre de Usuario").pack(pady=5)
        entry_usuario = ttk.Entry(ventana_mod)
        entry_usuario.insert(0, valores[1])  # Precargar valor
        entry_usuario.pack(pady=5)

        tk.Label(ventana_mod, text="Contraseña").pack(pady=5)
        entry_contrasena = ttk.Entry(ventana_mod, show='*')
        entry_contrasena.insert(0, valores[2])  # Precargar valor
        entry_contrasena.pack(pady=5)

        tk.Label(ventana_mod, text="Email").pack(pady=5)
        entry_email = ttk.Entry(ventana_mod)
        entry_email.insert(0, valores[4])  # Precargar valor
        entry_email.pack(pady=5)

        tk.Label(ventana_mod, text="Rol (1 para admin, 0 para cliente)").pack(pady=5)
        entry_rol = ttk.Entry(ventana_mod)
        entry_rol.insert(0, valores[3])  # Precargar valor
        entry_rol.pack(pady=5)

        # Botón para guardar cambios
        boton = tk.Button(ventana_mod, text="Guardar Cambios", command=lambda: guardarcambios())
        boton.pack(pady=10)
        


        def guardarcambios():
            usuario = entry_usuario.get()
            contrasena = entry_contrasena.get()
            email = entry_email.get()
			
            try:
            	rol = int(entry_rol.get())
				
            except ValueError:
                messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
                return

    # Validar los datos antes de modificar el usuario
            if validar_datos(usuario, contrasena, email, rol):
                try:
                   user_id = int(usuario_id)
                   usuario_modificado = User(usuario, contrasena, rol, email)
                   usuario_modificado.id = user_id

                # Llamada a la función para modificar en la base de datos
                   sql.modificarUsuario(usuario_modificado)
                   usuarios = sql.listarUsuarios()
                   for item in tree.get_children():
                        tree.delete(item)
                   for usuario in usuarios:
                        tree.insert('', 'end', values=(usuario.id, usuario.usuario, usuario.contrasena, usuario.rol, usuario.email))

                   ventana_mod.destroy()  # Cerrar la ventana de modificación
                   messagebox.showinfo("Éxito", "Usuario modificado con éxito.")

                except Exception as exc:
                    messagebox.showerror("Error", f"Error al guardar los cambios: {exc}")




def ventana_moduser(lienzo):
        lienzo.destroy()
        lienzo = tk.Tk()
        lienzo.geometry("1000x600")
        lienzo.title("Modificar Usuario")

		# Crear el Treeview para listar usuarios
        tree = ttk.Treeview(lienzo, columns=('ID', 'Usuario', 'Contraseña', 'Rol', 'Email'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Usuario', text='Usuario')
        tree.heading('Contraseña', text='Contraseña')
        tree.heading('Rol', text='Rol')
        tree.heading('Email', text='Email')
        tree.pack(side='top', fill='both', expand=True)

		# Rellenar el Treeview con los usuarios de la base de datos
        usuarios = sql.listarUsuarios()
        for usuario in usuarios:
            tree.insert('', 'end', values=(usuario.id, usuario.usuario, usuario.contrasena, usuario.rol, usuario.email))

		# Crear un botón que actúa sobre el usuario seleccionado
        boton = tk.Button(lienzo, text="Modificar Usuario", command=lambda: modificar_usuario(tree))
        boton.pack(pady=10)
        
        botonMenu = tk.Button(lienzo, text="Menú", command = lambda: ventana_adm(lienzo))
        botonMenu.pack(pady=20)

        lienzo.mainloop()

def validar_datos(usuario, contrasena, email, rol):
        if not usuario.strip():
            messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
            return False
        if len(contrasena) < 5:
            messagebox.showerror("Error", "La contraseña debe tener al menos 5 caracteres.")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "El email no es válido.")
            return False
        if rol not in [0, 1]:
            messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
            return False
        return True



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

    def validar_datos(usuario, contrasena, email, rol):
        if not usuario.strip():
            messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
            return False
        if len(contrasena) < 5:
            messagebox.showerror("Error", "La contraseña debe tener al menos 5 caracteres.")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "El email no es válido.")
            return False
        if rol not in [0, 1]:
            messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
            return False
        return True





    # Función para enviar datos al conector SQL
    def agregar_usuario():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        email = entry_email.get()

        try:
            rol = int(entry_rol.get())

        except ValueError:
            messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
            return

		
        if validar_datos(usuario, contrasena, email, rol):
            nuevo_usuario = User(usuario, contrasena, rol, email)
            sql.usuarioNuevo(nuevo_usuario)
            messagebox.showinfo("Éxito", f"Usuario {usuario} agregado con éxito")
            lienzo.destroy()


    # Botón para agregar usuario
    tk.Button(lienzo, text="Agregar Usuario", command=agregar_usuario).pack(pady=10)
    
    tk.Button(lienzo, text="Menú", command= lambda: ventana_adm(lienzo)).pack(pady=10)
    lienzo.mainloop()


def ventana_deluser(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x400")
    lienzo.title("Eliminar Usuario")

    tree = ttk.Treeview(lienzo, columns=('ID', 'Usuario', 'Rol', 'Email'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Rol', text='Rol')
    tree.heading('Email', text='Email')
    tree.pack(side='top', fill='both', expand=True)

    usuarios = sql.listarUsuarios()
    for usuario in usuarios:
        tree.insert('', 'end', values=(usuario.id, usuario.usuario, usuario.rol, usuario.email))

    def eliminar_usuario_seleccionado():
        seleccion = tree.selection()
        if seleccion:
            item = tree.item(seleccion)
            usuario_id = item['values'][0]
            if messagebox.askyesno("Confirmación", f"¿Está seguro de eliminar el usuario {item['values'][1]}?"):
                sql.eliminarUsuario(usuario_id)
                tree.delete(seleccion)

    boton = tk.Button(lienzo, text="Eliminar usuario seleccionado", command=eliminar_usuario_seleccionado)
    boton.pack(pady=10)
    
    botonMenu = tk.Button(lienzo, text="Menu", command= lambda: ventana_adm(lienzo))
    botonMenu.pack(pady =10)

    lienzo.mainloop()


def checkLogin(lienzo, username, password):
	
	usuario = sql.validarusuario(username, password)
	
	if usuario == "user_admin":
		
		ventana_adm(lienzo)
		
	elif usuario == "user_cliente":
		
		
		idUsuario = sql.obtenerIdCliente(username, password)
		
		ventana_user(lienzo, idUsuario)
		
	else:
		messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def salirAlLogin(lienzo):
	lienzo.destroy()
	
	
	
	login()


def registrarUsuario():
    
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


    
    entry_rol = ttk.Entry(lienzo)
    entry_rol.insert(0,0)
    

    def validar_datos(usuario, contrasena, email, rol):
        if not usuario.strip():
            messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
            return False
        if len(contrasena) < 5:
            messagebox.showerror("Error", "La contraseña debe tener al menos 5 caracteres.")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "El email no es válido.")
            return False
        if rol not in [0, 1]:
            messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
            return False
        return True





    # Función para enviar datos al conector SQL
    def agregar_usuario():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        email = entry_email.get()

        try:
            rol = int(entry_rol.get())

        except ValueError:
            messagebox.showerror("Error", "El rol debe ser 1 (admin) o 0 (cliente).")
            return

		
        if validar_datos(usuario, contrasena, email, rol):
            nuevo_usuario = User(usuario, contrasena, rol, email)
            sql.usuarioNuevo(nuevo_usuario)
            messagebox.showinfo("Éxito", f"Usuario {usuario} agregado con éxito")
            lienzo.destroy()


    # Botón para agregar usuario
    tk.Button(lienzo, text="Agregar Usuario", command=agregar_usuario).pack(pady=10)
    


def login():
		try:
			lienzo = Tk()
			lienzo.geometry("800x400")
			lienzo.title("LOGIN")
                  
			try:
				imagen = Image.open(r"imagen_agencia.jpg")
				imagen = imagen.resize((150, 150), Image.LANCZOS)  # Ajusta el tamaño de la imagen
				imagen_tk = ImageTk.PhotoImage(imagen)

				# Crear un widget Label para mostrar la imagen
				label_imagen = Label(lienzo, image=imagen_tk)
				label_imagen.image = imagen_tk  # Necesario para mantener la referencia a la imagen
				label_imagen.grid(row=0, column=0, padx=10, pady=10)  # Usamos grid para que no entre en conflicto con el siguiente formulario

			except Exception as e:
				print(f"Error al cargar la imagen: {e}")

            # recuadro de Login
            # recuadro de Login
			groupbox = LabelFrame(lienzo, text="Login", padx=5, pady=5)
			groupbox.grid(column=0, row=2, padx=220, pady=20)

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
			Button(groupbox, text="Registrarme", command = lambda : registrarUsuario()).grid(row=10, column=1, pady= 10)
            
					

            # recuadro de paquetes

			lienzo.mainloop()


		except ValueError as error:
			print("Error al mostrar la interfaz, error: {}".format(error))

class LoginUsuario:
	
	
	login()

