#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:24:58 2024

@author: avakonopka
"""
import numpy
import pprint
import requests
import sys
import csv

loc = [
    "Buenos Aires, Argentina",
    "Guangzhou, China",
    "Wichita, Kansas",
    "Niskayuna, New York",
    "Gwangmyeong, South Korea",
    "Taipei, Taiwan",
    "Nanaimo, British Columbia",
    "Chennai, India",
    "Barrington, Illinois",
    "Littleton, Colorado",
    "Peterhead, Scotland",
    "Vizag, India",
    "Des Moines, Iowa",
    "Beijing, China",
    "Killeen, Texas",
    "Morehead City, North Carolina"
]

weatherdata = {}

for i in range(0, len(loc)):
    api_key = "61e5270bb7956752a6560b846baf51dc"
    city =  loc[i]

# Geolocate Peterhead, Scotland to get its latitude and longitude

    geo_URL = 'http://api.openweathermap.org/geo/1.0/direct'

    geo = f'{geo_URL}?q={city}&limit=5&appid={api_key}'
    resp = requests.get( geo )

    if resp.status_code != 200: # Failure?
        print( f'Error geocoding {city}: {resp.status_code}' )
        sys.exit( 1 )

# OpenWeatherMap returns a list of matching cities, up to the limit specified
# in the API call; even if you only ask for one city (limit=5), it's still
# returned as a 1-element list

    if len( resp.json() ) == 0: # No such city?
        print( f'Error locating city {city}; {resp.status_code}' )
        sys.exit( 2 )

    json = resp.json()
    if type( json ) == list: # List of cities?
        lat = json[ 0 ][ 'lat' ]
        lon = json[ 0 ][ 'lon' ]
    else: # Unknown city?
        print( f'Error, invalid data returned for city {city}, {resp.status_code}' )
        sys.exit( 3 )

# Use Peterhead's latitude and longitude to get its 5-day forecast in 3-hour
# blocks

    forecast_URL = 'http://api.openweathermap.org/data/2.5/forecast'
    forecast = f'{forecast_URL}?lat={lat}&lon={lon}&appid={api_key}'
    resp = requests.get( forecast )
    print( f'Error geocoding {city}: {resp.status_code}' )

    if resp.status_code != 200: # Failure?
        print( f'Error retrieving data: {resp.status_code}' )
        sys.exit( 4 )
    
# Pretty-print the resulting JSON forecast for the first 3 hour block

    print( f'{city}:' )
    data = resp.json()
    printer = pprint.PrettyPrinter( width=80, compact=True )
    printer.pprint( data[ 'list' ][ 0 ] )

    weatherdata[city] = data



#add city names from loc to dictionary  
city2=[]
for i in range(0, len(loc)):
    dict2 = {}
    dict2['City'] = loc[i]
    city2.append(dict2)  


for i in range(0, len(city2)):
    data= weatherdata[city2[i]['City']] 
    
    #find start of tomorrow
    for p in range(0,8):
        if '00:00:00' in data['list'][p]['dt_txt']:
            start = p
            break
    
    #create list of temp_min for next 4 days
    min_temp={}
    for s in range(1,5):
        mintemp= []
        for k in range(start*s + (s-1), start*s + (s-1)+ 8 ):
            mintemp.append(data['list'][k]['main']['temp_min'])
        min_temp[s] = mintemp

    #create list of temp_max for next 4 days
    max_temp={}
    for s in range(1,5):
        maxtemp= []
        for k in range(start*s + (s-1), start*s + (s-1)+ 8 ):
            maxtemp.append(data['list'][k]['main']['temp_max'])
        max_temp[s] = maxtemp
    
    #find min and max temps for each of the next 4 days    
    mindailytemp=[]
    maxdailytemp=[]
    for n in range(1,5):
        mindailytemp.append(min(min_temp[n]))
        maxdailytemp.append(max(max_temp[n]))

    #convert from Kelvin to Celsius
    for w in range(0,4):
        mindailytemp[w] = round((mindailytemp[w] - 273.15),2)
        maxdailytemp[w] = round((maxdailytemp[w] - 273.15),2)

    #find avg min and max temps for next 4 days
    avgmintemp = round(numpy.average(mindailytemp), 2)
    avgmaxtemp = round(numpy.average(maxdailytemp), 2)
    avgmintemp = format(avgmintemp, '.2f')
    avgmaxtemp = format(avgmaxtemp, '.2f')

    #assign min, max, and avg values to their cities in city2 dictionary
    for l in range(0,4):
        city2[i]['Min ' + str(l+1)] = format(mindailytemp[l], '.2f')
        city2[i]['Max ' + str(l+1)] = format(maxdailytemp[l], '.2f')
    city2[i]['Min Avg'] = avgmintemp
    city2[i]['Max Avg'] = avgmaxtemp
    


#write to csv
fields = ['City','Min 1','Max 1','Min 2','Max 2','Min 3','Max 3','Min 4','Max 4','Min Avg','Max Avg']
with open('temp.csv', 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(city2)
    
    
file = "temp.csv"
opened = open(file, "r")
readed = csv.reader(opened, delimiter=",")
for row in readed:
    print(row)




weatherdata["Buenos Aires, Argentina"]
