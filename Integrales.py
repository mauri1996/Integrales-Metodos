# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 17:15:23 2022

@author: Daysi
"""
from tkinter import *
import tkinter.font as tkFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from math import *
from sympy import *

background = '#E8F8F5'

ventana = Tk()
ventana.geometry('1366x768')
ventana.title('Integrales')
ventana.config(bg=background)
ventana.resizable(0,0)

def graficarTrapecio():
    
    a1=int(txt_a.get())
    b1=int(txt_b.get())
    m_ = variador_de_frecuencia.get()
    H=abs((a1-b1)/m_)
    funcion = txt_entrada.get()
    x_i = np.linspace(a1, b1, m_+1)    
    f_i = []
    
    for x in x_i:                                               
        f_i.append(eval(funcion))    
    
    tbl0=Frame(ventana)
    tbl0.place(x=250,y=685)
    tb0=NavigationToolbar2Tk(canvas_funcion_trapecio,tbl0)
    
    grafica_funcion_trapecio.clear()
    grafica_funcion_trapecio.set_title("Trapecio",fontweight='bold',color='black',fontsize=10)
    grafica_funcion_trapecio.plot(x_i,f_i,label='Función',color='b')        
    grafica_funcion_trapecio.text(a1+0.5,f_i[0]-0.5, 'Integral:'+ str(round(calculateTrapecio(a1,b1,H,m_,funcion),2)),verticalalignment='center', fontsize=10,  color='red')
    grafica_funcion_trapecio.legend(loc='lower right')
    stems = grafica_funcion_trapecio.stem(x_i, f_i, linefmt='k-')
    line, = grafica_funcion_trapecio.plot(x_i, f_i, color='k')
    
    grafica_funcion_trapecio.set_xlim([a1-2, b1+2])
    funcion_trapecio.canvas.toolbar_visible = False
    funcion_trapecio.canvas.draw_idle()
    
    return x_i,f_i

def graficar(val='1'):
    graficarTrapecio()
    graficarPunto()
    graficarError()
    
def graficarPunto():

    a1=int(txt_a.get())
    b1=int(txt_b.get())
    m_ = variador_de_frecuencia.get()
    
    H=abs((a1-b1)/m_)    
    funcion = txt_entrada.get()
    
    x_i, f_i ,suma = calculatePunto(a1,b1,H,m_,funcion)
    
    tbl2=Frame(ventana)
    tbl2.place(x=250,y=375)
    tb2=NavigationToolbar2Tk(canvas_funcion_punto_medio,tbl2)
    
    grafica_funcion_punto_medio.clear()
    grafica_funcion_punto_medio.set_title("Punto medio",fontweight='bold',color='black',fontsize=10)
    grafica_funcion_punto_medio.plot(x_i,f_i,label='Función',color='b')    
    grafica_funcion_punto_medio.text(a1+0.5,f_i[0]-0.5, 'Integral:'+ str(round(suma,2)),verticalalignment='center', fontsize=10,  color='red')
    grafica_funcion_punto_medio.legend(loc='lower right')
    
    f_rectangule = []
    x_rectangule = []

    for x in x_i:    
        x_rectangule.append(x-(H/2))
        f_rectangule.append(eval(funcion))
        x_rectangule.append(x)
        f_rectangule.append(eval(funcion))
        x_rectangule.append(x+(H/2))
        f_rectangule.append(eval(funcion))
    
    line, = grafica_funcion_punto_medio.plot( x_rectangule, f_rectangule, color='grey')
    stems1 = grafica_funcion_punto_medio.stem(x_rectangule, f_rectangule, linefmt='grey')
    
    stems = grafica_funcion_punto_medio.stem(x_i, f_i, linefmt='k--', markerfmt='Dr')
    
    grafica_funcion_punto_medio.set_xlim([a1-2, b1+2])
    funcion_punto_medio.canvas.toolbar_visible = False
    funcion_punto_medio.canvas.draw_idle()
    
    return x_i,f_i

def graficarError():
    a1=int(txt_a.get())
    b1=int(txt_b.get())
    #m_ = variador_de_frecuencia.get()
    funcion = txt_entrada.get()
    
    ## Calculate real integal
    x = Symbol('x')
    real_inte = integrate(funcion,(x,a1,b1))
    
    x_punto = []
    y_punto = []
    
    x_trapecio = []
    y_trapecio = []    
    for m_ in range(2,101): # get H range
        H=abs((a1-b1)/m_)
        x_punto.append(H)
        x_trapecio.append(H)
        
        d1,d2,area_punto = calculatePunto(a1,b1,H,m_,funcion)
        area_trapecio = calculateTrapecio(a1, b1,H,m_,funcion)
        
        y_punto.append(abs(real_inte-area_punto))
        y_trapecio.append(abs(real_inte-area_trapecio))                
        
    tbl1=Frame(ventana)
    tbl1.place(x=700,y=375)
    tb1=NavigationToolbar2Tk(canvas_funcion_error,tbl1)
    
    grafica_funcion_error.clear()
    grafica_funcion_error.set_title("Error",fontweight='bold',color='black',fontsize=10)
    
    grafica_funcion_error.plot(x_punto,y_punto,label='Punto medio',color='b')    
    grafica_funcion_error.plot(x_trapecio,y_trapecio,label='Trapecio',color='r')
    grafica_funcion_error.set_xlabel('H')
    grafica_funcion_error.set_ylabel('Error')
    
    grafica_funcion_error.legend()
    funcion_error.canvas.toolbar_visible = False
    funcion_error.canvas.draw_idle()
    


def calculatePunto(a1,b1,H,m_,funcion):
    x_i = np.linspace(a1, b1, m_+1)    
    f_i = []
    
    suma=0.0
    for x in x_i:   
        f=eval(funcion)
        f_i.append(f)
        suma= suma+ float(abs(f*float(H)))
        
    return x_i,f_i,suma

def calculateTrapecio(a1, b1,H,m_,funcion):
    x=a1
    suma = eval(funcion)
    for i in range(0,m_-1,1):
        x = x + H
        suma = suma + 2*eval(funcion)
    x=b1
    suma = suma + eval(funcion)
    area = H*(suma/2)
    return area


#--------------------------------------------------------------------------------------------------------------------------------
# botones

boton1=Button(ventana,text="Calcular",padx=100,pady=0,bg='lightgray',fg='black',command=graficar,font=('Helvetica',12))
#boton1.place(x=600,y=10) #ubicacion del botton
boton1.grid(row=2, column=2) #ubicacion del botton

# Etiquetas
a = Label(ventana,text='a:',bg=background,fg='black',font=('Arial',12,'bold')).place(x=230,y=42)
b = Label(ventana,text='b:',bg=background,fg='black',font=('Arial',12,'bold')).place(x=410,y=42)
f = Label(ventana,text='Integrales',bg=background,fg='black',font=('Arial',12,'bold')).grid(pady=25, padx=45,row=0, column=0)  #x=800,y=45
f1 = Label(ventana,text='Función:',bg=background,fg='black',font=('Arial',12,'bold')).place(x=260,y=10)
m = Label(ventana,text='M',bg=background,fg='black',font=('Arial',15,'bold')).place(x=1180,y=90)

# Cuadros de texto de entrada
txt_entrada = Entry(ventana,bg='#CDCDCD') # Entrada de la función
txt_entrada.insert(END,'x**2')

txt_entrada.place(x=350,y=15)

txt_a = Entry(ventana,bg='#CDCDCD') # Entrada lim -inferior
txt_a.insert(END,'-2')
txt_a.place(x=251,y=45) 

txt_b = Entry(ventana,bg='#CDCDCD') # Entrada lim -superior
txt_b.insert(END,'2')
txt_b.place(x=432,y=45)


# Graficas
funcion_punto_medio = Figure(figsize=(4.4, 2.8),facecolor= background)#largo y algo de grafico
grafica_funcion_punto_medio = funcion_punto_medio.add_subplot(111)
grafica_funcion_punto_medio.set_title("Punto medio",fontweight='bold',color='black',fontsize=10)

funcion_trapecio = Figure(figsize=(4.4, 2.8),facecolor=background)
grafica_funcion_trapecio = funcion_trapecio.add_subplot(111)

grafica_funcion_trapecio.set_title("Trapecio",fontweight='bold',color='black',fontsize=10)

funcion_error = Figure(figsize=(4.4, 2.8),facecolor=background)#largo y algo de grafico
grafica_funcion_error = funcion_error.add_subplot(111)
grafica_funcion_error.set_title("Error",fontweight='bold',color='black',fontsize=10)

funcion_simp = Figure(figsize=(4.4, 2.8),facecolor=background)
grafica_funcion_simp = funcion_simp.add_subplot(111)
grafica_funcion_simp.set_title("Simpson",fontweight='bold',color='black',fontsize=10)


# Insertando las graficas en la interfaz
canvas_funcion_punto_medio = FigureCanvasTkAgg(funcion_punto_medio, ventana)
canvas_funcion_trapecio = FigureCanvasTkAgg(funcion_trapecio, ventana)
canvas_funcion_error = FigureCanvasTkAgg(funcion_error, ventana)
canvas_funcion_simp = FigureCanvasTkAgg(funcion_simp, ventana)



# Cuadros de graficas
canvas_funcion_punto_medio.get_tk_widget().grid(row=4, column=1)
canvas_funcion_trapecio.get_tk_widget().grid(row=5, column=1)
canvas_funcion_error.get_tk_widget().grid(row=4, column=2)
canvas_funcion_simp.get_tk_widget().grid(pady=30,row=5, column=2)


# Scroll
variador_de_frecuencia = Scale(ventana, from_=2, to=100,bg='#EAEAEA',
                               length=500,tickinterval=9,command=graficar)
variador_de_frecuencia.place(x=1150,y=120) #posisicon del scroll


ventana.mainloop()