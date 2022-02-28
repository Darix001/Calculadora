import sqlite3, json, traceback
from math import *
from datetime import datetime
import PySimpleGUI as sg
margins = (30,30)
database = "Historial.db"
def getquery(query):
	try:
		cursor.execute(query)
		return cursor.fetchall()
		con.commit()
	except Exception as e:
		tb = traceback.format_exc()
		print(f"ERROR: ", e, tb)

def setquery(query, confirm):
	try:
		cursor.execute(query)
		if confirm>0:
			con.commit()
		else:
			con.rollback()
		return cursor.rowcount
	except Exception as e:
		tb = traceback.format_exc()
		print(f"ERROR: ", e, tb)

def getjson(string):
	try:
		with open(string) as f: 
			return json.load(f)
	except Exception as e:
		tb = traceback.format_exc()
		print("Error:", e, tb)
		return {}

def savejson(dic, file):
	try:
		with open(file, 'w') as f: 
			json.dump(dic, f, indent=4)
	except Exception as e:
		tb = traceback.format_exc()
		sg.popup_error(f"Error: ", e, tb)
		print("Error:", e, tb)

def getTables():
	results=getquery("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
	tables=[]
	for result in results:
		if result[0]!="sqlite_sequence":
			tables.append(result[0])
	return tables

def CreateTable(table, columns):

	query="CREATE TABLE IF NOT EXISTS {} (".format(table)
	for x,column in enumerate(columns):
		if x+1==len(columns):
			query+="{} {})".format(column, columns[column])
		else:
			query+="{} {}, ".format(column, columns[column])
	setquery(query, 1)

def getIDs(table):
	ids = []
	rows = getquery("SELECT ID FROM {}".format(table))
	for row in rows:
		ids.append(row[0])
	return ids

def cant_rows(table):
	return getquery("SELECT COUNT(*) FROM {}".format(table))[0][0]

def DropTable(table, confirm):
	setquery("DROP TABLE IF EXISTS {}".format(table), confirm)

def AddColumn(table, column_def):
	for col in column_def:
		setquery("ALTER TABLE {} Add Column {} {}".format(
			table, col, column_def[col]),
		1)
def RenameTable(table, newname):
	setquery("ALTER TABLE {} RENAME TO {}".format(table, newname), 1)

def RenameColumn(table, column, new_column_name):
	setquery("ALTER TABLE {} RENAME COLUMN {} TO {}".format(
		table, column, new_column_name), 1)
def DropColumn(table, column):
	setquery("ALTER TABLE {} DROP COLUMN {}".format(table, column), 1)

def getcolumns(table):
	results=getquery("PRAGMA table_info({})".format(table))
	columns=[]
	datatype=[]
	for result in results:
		columns.append(result[1])
		datatype.append(result[2])
	return dict(zip(columns,datatype))

def Delete_from_table(table, confirm):
	setquery("DELETE *FROM " + table, confirm)

def Delete_where(table, column_condition, value_condition, confirm):
	setquery("DELETE FROM {} WHERE {}='{}'".format(table, column_condition
		, value_condition), confirm)

def Insert(table, list_of_columns, list_of_values, confirm):
	setquery("INSERT INTO {} ({}) VALUES {}".format(table,
	", ".join(list_of_columns), tuple(list_of_values)), confirm)

		
def Update(table, columns_values, column_condition, value_condition, confirm):
	values=str(columns_values)
	changes={
	":":"=",
	"{":"",
	"}":"",
	",":",\n"
	}
	for change in changes:
		values=values.replace(change, changes[change])
	setquery("UPDATE {} SET\n {} WHERE {}='{}'".format(table, values,
		column_condition, value_condition), confirm)

def Select_All(table):
	return getquery("SELECT *FROM " + table)

def Select_Where(table, column_condition, value_condition):
	return getquery("SELECT *FROM {} WHERE {}='{}'".format(table,
		column_condition, value_condition))

con=sqlite3.connect(database)
cursor=con.cursor()

font = 'Times New Roman'
title = (font, 20, 'bold')
text = (font, 16)
sg.theme('DarkAmber')
sg.set_options(font=text)

def get_edad(fechanac):
	if validate(fechanac):
		fechanacimiento=datetime.strptime(fechanac,"%d-%m-%Y")
		año = (fechanacimiento.year)
		mes = (fechanacimiento.month)
		dia = (fechanacimiento.day)
		añoac = (datetime.today().year)
		mesac = (datetime.today().month)
		diac = (datetime.today().day)
		edad=añoac-año
		if mes>mesac:
			edad = edad - 1
		else:
			if mes==mesac:
				if dia>diac:
					edad = edad - 1
		return edad
	else:
		return 0
def validatetime(date):
	try:
		datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
	except Exception as e:
		return False
	else:
		return True

def validate(string):
	try:
		date = datetime.strptime(string, "%d-%m-%Y")
	except Exception as e:
		tb=traceback.format_exc()
		print(f"ERROR: ", e, tb)
		return False
	else:
		return True

def Columns_Size(table, add=0):
	columns=list(getcolumns(table).keys())
	if add!=0:
		return list(len(column)+add for column in columns)
	else:
		return list(len(column) for column in columns)

def Max_Column_Size(table):
	lens=Columns_Size(table)
	lens.sort()
	return lens[len(lens)-1]

def get_len_Strings(strings):
	return [len(string) for string in strings]

def get_key(dic, val):
	for x,key in enumerate(dic):
		if dic[key]==val:
			return key
			break
		
		elif x+1==len(dic) and dic[key]!=val:
			return ""

def Order_By_Columns(list_of_rows, list_of_columns):
	table_dict={}
	for column in list_of_columns:
		table_dict[column]=[]
	
	for r,row in enumerate(list_of_rows):
		for c,column in enumerate(list_of_columns):
			table_dict[column].append(row[c])

	return table_dict

def get_datetype(table):
	tables=getTables()
	tables.remove(table)
	explication="Cuando una columna se enlaza a otra, esta solo aceptará valores que pertenezcan a la columna que se relaciona."
	choosen=set()
	layout=[
	[sg.Table(tooltip="Escoja un tipo de dato", key="Dato", bind_return_key=True,
	headings=["Tipo de Dato", "Descripción"], values=list(datetypes.items()), justification="c")],
	[sg.Checkbox(text='Conectar a la columna:', default=False, size=(16,1), enable_events=True, key="Relate"),
	sg.Combo(values=[], readonly=True, size=(16,1), disabled=True, key="columna")],
	[sg.T('Que pertenece a la Tabla:'), sg.Combo(values=tables, key="tabla", size=(17,1), enable_events=True, readonly=True, disabled=True)],
	[sg.B("Escojer"), sg.B("Salir")]
	]
	win = sg.Window("Escoja un tipo de dato", layout, margins=(30,30))
	while True:

		even, dat = win.read()
		if even in (sg.WIN_CLOSED, "Dato", "Escojer", "Salir"):
			try:
				if len(dat['Dato'])!=0:
					choosen = win['Dato'].get()[dat['Dato'][0]]
					if win['Relate'].get() and bool(dat['tabla']) and bool(dat['columna']):
						choosen[1]+=" REFERENCES {}({})".format(dat['tabla'], dat['columna'])

				else:
					choosen==[""]
			except TypeError as e:
				choosen==[""]
			finally:
				win.close()
				break
		else:
			if even=="Relate":
				for op in ['tabla', 'columna']:
					win[op](disabled = not win[even].get())

			elif even=="tabla":
				win['columna'](values=list(getcolumns(dat['tabla'])))

	return choosen

def Select_Columns(table, columns):
	values=[]
	results = getquery("SELECT {} FROM {}".format(",".join(columns), table))
	for row in results:
		values.append(row[0])

	return values

table="Historial"
columns={
	"ID":"INTEGER PRIMARY KEY",
	"Calculo":"text",
	"Fecha":"Datetime"
	}

CreateTable(table, columns)

datetypes={
"int":"Números enteros",
"text":"Texto",
"DateTime":"Fecha y Hora",
"Date":"Fecha",
"Decimal":"Números Decimales",
"Money":"Dinero"
}