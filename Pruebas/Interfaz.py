#GRUPO 10: Cifuentes Juan, Ortiz Alvaro, Maidana Emilio
#DIA Y HORARIO: 12/11 - 20:40 HS
#Crear un programa para el manejo de viajes de una empresa de turismo teniendo en cuenta
#los siguientes aspectos:

#1) El sistema debe ser de acceso restringido sólo para algunas opciones especiales (a
#considerar según el grupo de trabajo)
#2) Planificación de viajes, destinos, duración y precios de los mismos
#3) Salida de comprobantes por pantalla.






from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LoginUsuario:
    def login():
        try:
            lienzo = Tk()
            lienzo.geometry("800x400")
            lienzo.title("Login")

            #recuadro de Login
            groupbox = LabelFrame(lienzo, text="Login", padx=5, pady=5 )
            groupbox.grid(column=0, row=0, padx=220, pady=20)
            labelname= Label(groupbox, text="Username: ", width=13, font=("Arial", 12)).grid(row=0,column=0)
            textboxusername= Entry(groupbox).grid(row = 0, column = 2)

            groupbox.grid(column=0, row=0, columnspan=10)
            labelpw = Label(groupbox, text="Password: ", width=13, font=("Arial", 12)).grid(row=1, column=0)
            textboxpw = Entry(groupbox).grid(row=1, column=2)
            
            Button(groupbox,text="Soy admin", width= 10).grid(row=2, column = 0)
            Button(groupbox, text="Soy Cliente", width=10).grid(row=2, column=2)

            #recuadro de paquetes
            usuario=0

            groupbox = LabelFrame(lienzo, text="Seleccione el destino", padx=5, pady=5)
            groupbox.grid(row=1, column=0, padx=0, pady=0)
            labelDest = Label(groupbox, text="Destino ", width=13, font=("Arial", 12)).grid(row=1, column=0)
            labeldestino = Label(groupbox, text="Seleccione el destino: ", width=20, font=("Arial", 12)).grid(row=1,column=0)
            select_destino = tk.StringVar()
            combo = ttk.Combobox(lienzo, values=["Copacabana", "United States", "Islas Galapagos", "Buenos Aires"],width=30, textvariable=select_destino).grid(row=1, column=1)




            lienzo.mainloop()


        except ValueError as error:
            print("Error al mostrar la interfaz, error: {}".format(error))
    login()