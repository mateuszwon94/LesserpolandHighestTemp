#!/usr/bin/python3
# -*- coding: utf8 -*-

from time import sleep
import urllib.request
import urllib
import json
from datetime import datetime
from timeit import default_timer as timer

request = 'http://mech.fis.agh.edu.pl/meteo/rest/json/info/'
response = urllib.request.urlopen(request)
stations = eval(str(json.load(response)))
stationsError = []
request = "http://mech.fis.agh.edu.pl/meteo/rest/json/last/"
maxTemp = -100
maxTempTimes = []
while True:
    try:
        start = timer()
        for station in stations:
            print("Odczytuje dane ze stacji: " + station["name"] + " (" + station["station"] + ").")
            try:
                curTime = datetime.now().strftime('%Y-%m-%d %H:%M')
                try:
                    response = urllib.request.urlopen(request + station["station"])
                except (TimeoutError, urllib.error.URLError):
                    print("\tBLAD! Brak polaczenia internetowego!")
                    continue
                
                data = str(json.load(response))
                if data != "[]":
                    data = eval(data)
                else:
                    stationsError.append(station)
                    print("\tBLAD! Pomijam stacje w przyszlosci.")
                    continue
                try:
                    curTemp = float(data[0]["data"]["ta"])
                except TypeError:
                    print("\tBLAD! Nie mozna odczytac temperatury.")
                    continue
                if curTemp == maxTemp:
                    maxTempTimes[station["name"]] = curTime
                elif curTemp > maxTemp:
                    maxTemp = curTemp
                    maxTempTimes = {station["name"]: curTime}
            except:
                "\tBLAD!"
                continue
        
        print("\nMaksymalna odczytana temperatura to: " + str(maxTemp))
        print("Zmierzono ja na nastepujacych stacjach:")
        for stationName in maxTempTimes.keys():
            print("\t"+ stationName + " - " + maxTempTimes[stationName])
        print("\n\n\n\n\n")

        for badStation in stationsError:
            stations.remove(badStation)
        stationsError.clear()

        stop = timer()
        elapsed = stop-start
        if elapsed < 60:
            sleep(60 - elapsed)
    except KeyboardInterrupt:
        break

input("Nacisnij ENTER by wyjsc")