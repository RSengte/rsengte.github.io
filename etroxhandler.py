import datetime
import math
import requests

class ETROX():
    def _init(mysillyobject):
        mysillyobject
        
    def getAllCompanies(mysillyobject):
        companies = {}
        companies['Erixx'] ='erixx'
        companies['Metronom']= 'metronom'
        companies['Enno'] = 'enno'
        return companies
        
    def getStations(mysillyobject, company: str):
        #load webseite once, to get the cookie, otherwiese livedata will responce with not allowed
        response = requests.get('https://www.erixx.de')
        #print(response.cookies)
        #get all stations from select train
        responseLive = requests.get(f"https://www.erixx.de/livedata/etc?type=stationen&product={company}",cookies=response.cookies)
        stations = responseLive.json()
        
        #show all stations
        #for station in stations['bhf']:
        #   print (station['name'])
            
        return stations
     
    def getStationInfo(mysillyobject, company: str, station: str):
        #we can do all the functions with different train companies (enno, erixx or metronom)
        #load webseite once, to get the cookie, otherwiese livedata will responce with not allowed
        response = requests.get('https://www.erixx.de')
        #get information from station
        responseLive = requests.get(f"https://www.erixx.de/livedata/etc?type=stationsauskunft&bhf={station}&product={company}", cookies=response.cookies)
        stationInfo = responseLive.json()
        
        #if a array is not an array the for loop will not work
        arrayObject = []
        if "abfahrt" in stationInfo:
           if isinstance(stationInfo['abfahrt'], dict):
                arrayObject.append(stationInfo['abfahrt'])
           else:
                arrayObject = stationInfo['abfahrt']
            
        return arrayObject
        
    def getTrainString(mysillyobject, traininfo):

        canceled = traininfo['ausfall'] != 'false'
        sev = traininfo['sev']
        sevtext = ""
        if sev:
            sevtext = " :bus: Ersatzverkehr ist eingerichtet!"
        if canceled:
            return (f"<pre>:bangbang:{traininfo['linie']}({traininfo['zug']}) nach {traininfo['ziel']} Abfahrt {traininfo['zeit']} entfällt!{sevtext}</pre>" )
        delayed = not traininfo['prognose'].__contains__('pünktlich')
        delay = ''
        if traininfo['prognosemin'] != 0:
            delay = f" +{traininfo['prognosemin']}"
        platform = ""
        if "gleis" in traininfo:
            platform = f" auf Gleis {traininfo['gleis']}"

        if "gleiswechsel" in traininfo:
            platform = f" abweichend auf Gleis {traininfo['gleiswechsel']}:exclamation:"
             
        #if a array is not an array the for loop will not work
        wagons = 0    
        if not traininfo['fahrzeuge']:
            wagons = 1
        elif (isinstance(traininfo['fahrzeuge']['fahrzeug'], dict)):
            wagons = 1
        else:
            wagons = len(traininfo['fahrzeuge']['fahrzeug'])
     
        return (f"<pre>{traininfo['linie']}({traininfo['zug']}) nach {traininfo['ziel']} Abfahrt {traininfo['zeit']}{delay}{platform} [{wagons} Wagen]</pre>" )

    def getAllTroubles(mysillyobject, company: str):
        response = requests.get('https://www.erixx.de')
        #get information from station
        responseLive = requests.get(f"https://www.erixx.de/livedata/etc?type=troublelist&product={company}", cookies=response.cookies)
        troubles = responseLive.json()
        return troubles
        
    def getTroubleString(mysillyobject, trouble):
        return f"<pre>{trouble['linie']}: {trouble['text']}</pre>"
#etroxhandler = ETROX()
#companies = etroxhandler.getAllCompanies()
#print(companies) 
#stations = etroxhandler.getStations('erixx')
#print(stations) 
#stationInfo = etroxhandler.getStationInfo('erixx', 'HHIO')
#for abfahrt in stationInfo:
#    text = etroxhandler.getTrainString(abfahrt)
#    print(text)
#troubles = etroxhandler.getAllTroubles('erixx')
#for trouble in troubles:
#    text = etroxhandler.getTroubleString(trouble)
#    print(text)
#
