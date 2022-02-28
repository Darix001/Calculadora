from DB import *
import Historial, pyperclip

def prom(num_list):
	return avg(num_list)

def avg(num_list):
	return sum(num_list)/len(num_list)

def show_shortcuts():
	keyboard_shortcuts={
	"ANS":"Ctrl + a",
	"Ayuda":"F12",
	"Calcular":"Enter",
	"Copiar":"Ctrl + c",
	"Función":"Ctrl + f",
	"Historial":"Ctrl + h",
	"Limpiar":"F5",
	"Mostrar en el Campo":"Ctrl + m",
	}
	ly=[
	[sg.Table(headings=["Acción", "Teclas"], values=list(keyboard_shortcuts.items()), 
	num_rows=len(keyboard_shortcuts), auto_size_columns=True, justification='c')],
	[sg.OK()]
	]
	sevent, sdata = sg.Window("Atajos del Teclado", ly, modal=True, margins=(10,10),
	finalize=True, element_justification='c').read(close=True)

def show_functions(return_val=False):
	math_dict={
	'Convertir x grados a radianes': 'radians(x)',
	'Convertir x radianes a grados': 'degrees(x)',
	'Coseno': 'Cos(x)',
	'Factorial de x': 'factorial(x)',
	'Logaritmo de x base 10': 'Log10(x)',
	'Logaritmo de x base y': 'Log(x, y)',
	'No. Euler elevado a x': 'Exp(x)',
	'Número Euler': 'e',
	'Número π(3.14)': 'pi',
	'Potencia': 'Pow(base, exponente)',
	'Promedio':'AVG([x,y,z])',
	'Raíz Cuadrada': 'sqrt(x)',
	'Saber si x es infinito': 'isinf(x)',
	'Seno': 'Sen(x)',
	'Sumar lista de Números':'sum([x,y,z])',
	'Tangente': 'Tan(x)',
	'Valor Mínimo':'min([x,y,z])',
	}

	aevent, adata = sg.Window('Atajos del Teclado', [
	[sg.T('Datos del Teclado', font=text+('bold',))],
	[sg.Table(values=list(math_dict.items()), headings=["Método Matemático", "Nombre Clave"],
	col_widths=[max([len(row) for row in list(math_dict)]), max([len(row) for row in list(math_dict.values())])],
	justification='c', key="Función", bind_return_key=True)],
	[sg.OK(), sg.B("Cancelar", visible=return_val)]
	], element_justification='c', margins=margins).read(close=True)

	if return_val and aevent not in ("Cancelar", sg.WIN_CLOSED) and bool(adata["Función"]):
		return list(math_dict.values())[adata['Función'][0]]
	else:
		return ""

def Insert_new_History(calculo, fecha):	
	Insert(table, list(columns), [cant_rows(table)+1, calculo, fecha], 1)

def Mainlayout():
	menu_def=[
	["Opciones", ["Calcular", "Salir", "Limpiar"]],
	["Mostrar", ["Historial", "Resultado Anterior", "Ayuda"]],
	["Insertar...",["Función"]]
	]
	column=[
	[sg.Menu(menu_def)],
	[sg.T('Introduzca la operación:', font=title)],
	[sg.Input(key='Input', size=(50,1), text_color='white')],
	[
	sg.Checkbox("Limpiar Automáticamente", default=True, key="Auto_Clean",
		tooltip="Si se marca, el campo se limpiará Automáticamente."),
	sg.VerticalSeparator(),
	sg.Checkbox('Redondear:', default=False, key="round", 
		tooltip="Redondear Resultado."),
	sg.Spin([i for i in range(21)], size=(4,0), initial_value=0, key="decimaldigits",
		tooltip="Cantidad de Cifras Decimales a redondear.")
	],
	[sg.T('Resultados:', font=title, justification='center')],
	[sg.Listbox([], key='Resultado', size=(50,10), change_submits=True, right_click_menu=["menu", ["Copiar", "Mostrar en el Campo"]])],
	[sg.B("Calcular", visible=False, bind_return_key=True)]
	]

	layout=[[sg.Column(column, element_justification='center')]]
	return layout
	

if __name__ == '__main__':
	sg.theme('DarkAmber')
	sg.set_options(font=text)
	try:
		window = sg.Window('Calculadora (ventana Principal)', Mainlayout(), margins=(30, 30), 
		return_keyboard_events=True, icon="icon.ico", finalize=True, enable_close_attempted_event=True)
		resultado=set()
		
		while True:

			event, data = window.read()
			
			if event not in ('Salir', "-WINDOW CLOSE ATTEMPTED-",):
				print(event)
				if event=="Calcular":
					original=data['Input']
					try:
						if any(char.isalpha() for char in data['Input']):
							data['Input']=data['Input'].lower()
						
						if data['Input']=="" or data['Input'].isspace():
							sg.popup_error("Error, Campo Vacío")
						else:
							resultado=data['Input']
							resultado=eval(data['Input'])
							if window['round'].get():
								cantdigits=int(data['decimaldigits'])
								resultado=round(resultado, cantdigits)

					except Exception as e:
						tb = traceback.format_exc()
						sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
					finally:
						window['Resultado'](values=["{} = {}".format(original, resultado)] + window['Resultado'].get_list_values())
						if window['Auto_Clean'].get(): window['Input']("")
						Insert_new_History("{} = {}".format(original, resultado), str(datetime.today()))
				
				elif event in ("Limpiar", "F5:116"):
					window['Input']("")
					window['Resultado'](values=[])
				
				elif event in ("ANS", "a:65"):
					window['Input'].Update(data['Input']+str(resultado))

				elif event in ("Historial", "h:72"):
					Historial.Historial()

				elif event in ("Mostrar en el Campo", "m:77") and bool(data['Resultado']):
					window['Input'](data['Resultado'][0])

				elif event in ("Función", "f:70"):
					window['Input'](window['Input'].get() + show_functions(return_val=True))

				elif event in ("Copiar", "c:67") and bool(data['Resultado']) and window.FindElementWithFocus()==window['Resultado']:
					pyperclip.copy(data['Resultado'][0])
					sg.popup_ok("Copiado al Portapapeles.")

				elif event in ("Ayuda", "F12:123"):
					show_shortcuts()
			else:
				if sg.popup_yes_no('Desea Salir del programa') == 'Yes':
					break
					window.close()

	except Exception as e:
		tb = traceback.format_exc()
		sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
	else:
		print("Sucessfull Execution!")
main()