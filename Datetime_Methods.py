from datetime import datetime
import traceback

def get_zodiac_sign(fechanac):
	if validate(fechanac):
		fechanacimiento=datetime.strptime(fechanac,"%d-%m-%Y")
		año = (fechanacimiento.year)
		mes = (fechanacimiento.month)
		dia = (fechanacimiento.day)
		añoac = int (datetime.today().strftime('%Y'))
		mesac = int (datetime.today().strftime('%m'))
		diac = int (datetime.today().strftime('%d'))
		signo = str()
		if mes == 1:
		    if dia <=20:
		        signo= ('capricornio')
		    else:
		        signo ='Acuario'
		elif mes == 2:
		    if dia <=18:
		        signo ='Acuario'
		    else:
		        signo ='Piscis'
		elif mes == 3:
		    if dia <=20:
		        signo = 'piscis'
		    else: 
		        signo = 'Aries'
		elif mes == 4:
		    if dia <=20:
		        signo = 'Aries'
		    else: 
		        signo = 'Tauro'
		elif mes == 5:
		    if dia <=21:
		        signo = 'Tauro'
		    else: 
		        signo = 'Geminis'
		elif mes == 6:
		    if dia <=21:
		        signo = 'Geminis'
		    else: 
		        signo= 'Cancer'
		elif mes == 7:
		    if dia <=22:
		        signo= 'Cancer'
		    else: 
		        signo = 'Leo'
		elif mes == 8:
		    if dia <=23:
		        signo = 'Leo'
		    else: 
		        signo = 'Virgo'
		elif mes == 9:
		    if dia <=23:
		        signo = 'virgo'
		    else: 
		        signo = 'Libra'
		elif mes == 10:
		    if dia <=23:
		        signo = 'Libra'
		    else: 
		        signo = 'Escorpion'
		elif mes == 11:
		    if dia <=22:
		        signo = 'Escorpion'
		    else: 
		        signo = 'Sagitario'
		elif mes == 12:
		    if dia <=21:
		        signo = 'Sagitario'
		    else: 
		        signo = 'Capricornio'
		return signo
	else:
		return ""

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
		datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
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
