import sqlite3, json, traceback
from datetime import datetime
import random
margins = (30,30)
database = "Historial.db"
font = "Times New Roman"
title = (font, 20, 'bold')
text = (font, 16)

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
	results=getquery("SELECT name FROM sqlite_master WHERE type='table'; ")
	tables=[]
	for result in results:
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

def getcolumns(table):
	results=getquery("PRAGMA table_info({})".format(table))
	columns=[]
	datatype=[]
	for result in results:
		columns.append(result[1])
		datatype.append(result[2])
	return dict(zip(columns,datatype))

def Delete_from_table(table):
	setquery("DELETE *FROM " + table, 1)

def Insert(list_of_values, table):
	setquery("INSERT INTO {} ({}) VALUES {}".format(table, 
	", ".join(list(getcolumns(table).keys())), tuple(list_of_values)))
		
def Update(table, columns_values, column_condition, value_condition):
	values=""
	for x,column in enumerate(columns_values):
		if x+1==len(columns_values):
			values+="{} = '{}',\n".format(columnm, columns_values[column])
		else:
			values+="{} = '{}'\n".format(columnm, columns_values[column])
	
	setquery("UPDATE {} SET\n {} WHERE {}='{}'".format(table, values, 
		column_condition, value_condition))

def Select_All(table):
	return getquery("SELECT *FROM " + table)

def Select_Where(table, column_condition, value_condition):
	return getquery("SELECT *FROM {} WHERE {}='{}'".format(table,
		column_condition, value_condition))

con=sqlite3.connect(database)
cursor=con.cursor()
table="Historial"
columns={
	"ID":"int primary key",
	"Calculo":"text",
	"Fecha":"Datetime"
}
CreateTable(table, columns)

if __name__ == '__main__':
	pass