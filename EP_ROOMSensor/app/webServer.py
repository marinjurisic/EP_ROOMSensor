from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3

@app.route("/")
def index():
	import sys
	import Adafruit_DHT
	hum, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
	if hum is not None and temp is not None:
		hum  = round(hum, 1)
		temp = round(temp, 1)
		time = str(getLastTime())
		return render_template("index.html", temp=temp, hum=hum, time=time)
	else:
		return ("Nismo pronašli senzor!")

def getLastTime():
	conn = sqlite3.connect('../sensorDB.db')
	curs = conn.cursor()
	for row in curs.execute( "SELECT DATETIME(timestamp, 'localtime') FROM podaci ORDER BY timestamp DESC LIMIT 1"):
		time  = str(row[0])
	conn.close()
	return time

def getTime():
	conn  = sqlite3.connect('../sensorDB.db')
	curs  = conn.cursor()
	query = "SELECT TIME(timestamp, 'localtime')  FROM podaci ORDER BY timestamp DESC LIMIT 10" 
	curs.execute(query)
	time = curs.fetchall()
	conn.close()
	return time

def getTemp():
	conn  = sqlite3.connect('../sensorDB.db')
	curs  = conn.cursor()
	query = "SELECT temp  FROM podaci ORDER BY timestamp DESC LIMIT 10" 
	curs.execute(query)
	temp = curs.fetchall()
	conn.close()
	return temp

def getHum():
	conn  = sqlite3.connect('../sensorDB.db')
	curs  = conn.cursor()
	query = "SELECT hum  FROM podaci ORDER BY timestamp DESC LIMIT 10" 
	curs.execute(query)
	hum = curs.fetchall()
	conn.close()
	return hum



@app.route("/dijagrami")
def karte():
	time = getTime()
	temp = getTemp()
	hum  = getHum()
	templateData	= {
		'time' : time,
		'temp' : temp,
		'hum'  : hum
	}
	return render_template('dijagrami.html', **templateData) 

@app.route("/tablice", methods=['GET', 'POST'])
def goTablice():
	conn = sqlite3.connect('../sensorDB.db')
	curs = conn.cursor()
	if request.method == 'POST':
		if request.form.get('Svi_podaci') == 'Svi Podaci':
			query = "SELECT ROW_NUMBER() OVER(ORDER BY timestamp DESC) br, DATETIME(timestamp, 'localtime'), temp, hum FROM podaci ORDER BY timestamp DESC"
			curs.execute(query)
			data = curs.fetchall()
			conn.close()
			return render_template('tablice.html', data=data)
		elif request.form.get('Danas') == 'Danas':
			query = "SELECT ROW_NUMBER() OVER(ORDER BY timestamp DESC) br, DATETIME(timestamp, 'localtime'), temp, hum FROM podaci WHERE DATE(timestamp, 'localtime') = DATE('now')"
			curs.execute(query)
			data = curs.fetchall()
			conn.close()
			return render_template('tablice.html', data=data)
		elif request.form.get('Jucer') == 'Jučer':
			query = "SELECT ROW_NUMBER() OVER(ORDER BY timestamp DESC) br, DATETIME(timestamp, 'localtime'), temp, hum FROM podaci WHERE DATE(timestamp, 'localtime' ) = DATE('now', '-1 days')"
			curs.execute(query)
			data = curs.fetchall()
			conn.close()
			return render_template('tablice.html', data=data) 
	elif request.method == 'GET':
		return render_template('tablice.html')


if __name__ == "__main__" :
	app.run(host = '0.0.0.0', port = 8000, debug = True)
