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
import pyodbc

import sqlConnector as sql
#conecto a la base de datos



def ventana_user(lienzo):
	
	lienzo.destroy()
    
	lienzo = tk.Tk()
    
	lienzo.geometry("800x400")
    
	lienzo.title("User")
    
    #recuadro destino
	groupbox = LabelFrame(lienzo, text="Seleccione el destino", padx=5, pady=5)
    
	groupbox.grid(row=1, column=0, padx=0, pady=0)
    
	labelDest = Label(groupbox, text="Destino ", width=13, font=("Arial", 12)).grid(row=1, column=0)
    
	labeldestino = Label(groupbox, text="Seleccione el destino: ", width=20, font=("Arial", 12)).grid(row=1,column=0)
    
	select_destino = tk.StringVar()
    
	listaPaquetes = []
    
	destinosSQL = sql.listarPaquetes()
    
	for i in destinosSQL:
		listaPaquetes.append(i.destino)
    
	combo = ttk.Combobox(lienzo, values= listaPaquetes,width=30, textvariable=select_destino).grid(row=1, column=1)
	
	#paqueteSeleccionado = combo.bind("<<ComboboxSelected>>", sql.buscarPaquetePorId(combo.get()))
	
	#print(paqueteSeleccionado.destino)
	lienzo.mainloop()
    
	return





def ventana_adm(lienzo):
    lienzo.destroy()
    lienzo = tk.Tk()
    lienzo.geometry("550x200")
    lienzo.title("Administrador")
    groupbox = LabelFrame(lienzo, text="Seleccione una opcion", padx=50, pady=5)
    groupbox.grid(row=1, column=0, padx=0, pady=0)

    Button(groupbox, text="Editar Destino", width=20).grid(row=1, column=0)
    Button(groupbox, text="Agregar Destino", width=20).grid(row=1, column=1)
    Button(groupbox, text="Actualizar Destino", width=20).grid(row=1, column=2)
    
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
