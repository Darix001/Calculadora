import traceback
import PySimpleGUI as sg
import sqlite3, os, Datetime_Methods, pyperclip
from Extension import *
from datetime import datetime
rows=set()

def rows_by(order_by):
	if order_by=="Ascendente":order_by="ASC"
	if order_by=="Descendente":order_by="DESC"
	return getquery("SELECT *FROM {} ORDER BY FECHA {}".format(table, order_by))


def Mainlayout():
	global rows
	rows=rows_by("Ascendente")
	botones=["Salir", "Borrar Historial"]
	for x,btn in enumerate(botones):
		botones[x]=sg.Button(btn)

	radios=["Ascendente", "Descendente"]
	for x,rad in enumerate(radios):
		radios[x]=sg.Radio(rad, "Order_by", key=rad, size=(10,1), enable_events=True)

	menu=["Menu", ["Copiar Cálculo"]]
	
	column = [
	[sg.T("Historial", font=title)],
	[sg.T("Mostrar a partir de :"),
	sg.In("'Fecha'", key="date", size=(20,0)),
	sg.CalendarButton('Escoger Fecha'),
	sg.B(key="Search",  button_color=(sg.theme_background_color(),
	"gray"), image_filename="Lupa.png",
	image_size=(40, 37), image_subsample=2, border_width=1)],
	[sg.Table(values=rows, headings=list(columns), auto_size_columns=True,
	num_rows=15, change_submits=True, key=table, justification='c', right_click_menu=menu)],
	botones,
	radios
	]

	layout=[
	[sg.Column(column, element_justification='center')]
	]
	return layout
	
def Historial():
	sg.theme('DarkAmber')
	try:
		sg.set_options(font=text)

		windowh = sg.Window("Mostrar "+table, Mainlayout(), margins=(30, 30), icon="icon.ico",
		finalize=True, modal=True)
		
		while True:

			eventh, datah = windowh.read()
			
			if (eventh!='Salir' and eventh!=sg.WIN_CLOSED):
				
				for rad in ["Ascendente", "Descendente"]:
					if windowh[rad].get():
						get=windowh[table].get()
						if rad=="Descendente":
							get.sort(reverse=True)							
						else:
							get.sort()
						windowh[table](values=get)

				if eventh=="Borrar Historial":
					if sg.popup_yes_no("¿Desea Borrar el Historial?")=="Yes":
						DropTable(table, 1)
						CreateTable(table, columns)
						sg.popup_ok("Historial Eliminado")
						windowh[table].Update(values=rows_by("Ascendente"))
					else:
						sg.popup_ok("Operacion Cancelada")

				elif eventh=="Copiar Cálculo" and bool(datah[table]):
					pyperclip.copy(windowh[table].get()[datah[table][0]][1])
					sg.popup_ok("Copiado al Portapapeles.")

				elif eventh=="Search":
					if windowh['date'].get()=="'Fecha'" or datah['date']=="":
						sg.popup_error("Error, no ha seleccionado una fecha")
					else:
						date=windowh['date'].get()
						if Datetime_Methods.validatetime(date):
							date+=".0"
							date_rows=getquery("SELECT *FROM {} WHERE Fecha>'{}'".format(table, date))
							windowh[table].Update(values=date_rows)
							windowh.Refresh()
						else:
							sg.popup_error("Error en el formato de fecha")
							
			else:
				windowh.close()
				break
						
	except Exception as e:
		tb = traceback.format_exc()
		sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
	else:
		print("Sucessfull Execution!")

