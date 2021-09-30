import time
import sqlite3
import Adafruit_DHT

dbname='sensorDB.db'

sampleFreq = 1*3600

def getData():
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin      = 4
	hum, temp   = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum  = round(hum, 1)
		temp = round(temp, 1)
	return temp, hum


def logData(temp, hum):
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()
	curs.execute("INSERT INTO podaci VALUES(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()


def main():
	while True:
		temp, hum = getData()
		logData(temp, hum)
		time.sleep(sampleFreq)

main() 
