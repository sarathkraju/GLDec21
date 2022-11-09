import urllib.parse
from shapely.geometry import Polygon
from shapely.geometry import Point
import numpy as np
import json
# Imports MongoClient and GEOSPHERE for base level access to the local MongoDB and geospatial data
from pymongo import MongoClient, GEOSPHERE
# Imports datetime class to create timestamp for weather data storage
from datetime import datetime

print('############### CAPSTONE PROJECT ####################')
print('')
print('### RUNNING SETUP ###')
print('')
# getting input from client for loginUser
country = input('please enter country for setting up CabMe App: ')
print('')
city = input('please enter country for setting up CabMe App: ')
print('')
polygon=''

with urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?q="+ city +"+"+country+"&polygon_geojson=1&format=geojson") as url:
    geoJsondata = json.load(url)
    for item in geoJsondata['features']:
        if(item['geometry']['type'] == 'Polygon'):
           coordinates = item['geometry']['coordinates']
           polygon = Polygon(coordinates[0])           
           minx, miny, maxx, maxy = polygon.bounds
                                  
if polygon!='':
    RELATIVE_CONFIG_PATH = 'C:/Users/sarat/OneDrive/Documents/ACSE_IITM_GreatLearning/Capstone Project - Taxi Aggregator/config/'
    POINTS = []
    DB_NAME = 'CabMe'
    USER_COLLECTION = 'UserDetails'
    TAXI_COLLECTION = 'TaxiDetails'

    # This will initiate connection to the mongodb
    db_handle = MongoClient("mongodb+srv://GLCapstone:"  + urllib.parse.quote("Capstone@2022") + "@cluster0.tfzkg67.mongodb.net/test")

    # We drop the existing database including all the collections and data
    db_handle.drop_database(DB_NAME)

    # We recreate the database with the same name
    cabMe_dbh = db_handle[DB_NAME]

    # user data import
    # User document includes name, email and location
    # Reads UserDetails.json and loads them to user_collection
    with open(RELATIVE_CONFIG_PATH+USER_COLLECTION+'.json') as user_fh:
        # This loads the json file to user_data
        user_data = json.load(user_fh)

        for user in user_data:
            location = user['location']['coordinates']
            print(location)
            while len(POINTS) == 0 :
                pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
                if polygon.contains(pnt):            
                    POINTS.append(pnt)
            user['location']['coordinates'][0] = POINTS[0].x
            user['location']['coordinates'][1] = POINTS[0].y
            POINTS=[]        

        # This creates and return a pointer to the users collection
        user_collection = cabMe_dbh[USER_COLLECTION]
        # Create Index(es)
        user_collection.create_index([('location', GEOSPHERE)])
        # This inserts the data item as a document in the user collection
        if isinstance(user_data, list):
            user_collection.insert_many(user_data) 
        else:
            user_collection.insert_one(user_data)
        
    # Taxi data import
    # User document includes name, email, location and Type
    # Reads TaxiDetails.json and loads them to taxi_collection
    with open(RELATIVE_CONFIG_PATH+TAXI_COLLECTION+'.json') as taxi_fh:
        # This loads the json file to user_data
        taxi_data = json.load(taxi_fh)

        for taxi in taxi_data:
            location = taxi['location']['coordinates']
            print(location)
            while len(POINTS) == 0 :
                pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
                if polygon.contains(pnt):            
                    POINTS.append(pnt)
            taxi['location']['coordinates'][0] = POINTS[0].x
            taxi['location']['coordinates'][1] = POINTS[0].y
            POINTS=[]     

        # This creates and return a pointer to the users collection
        taxi_collection = cabMe_dbh[TAXI_COLLECTION]
        # Create Index(es)
        taxi_collection.create_index([('location', GEOSPHERE)])

        # This inserts the data item as a document in the user collection
        if isinstance(taxi_data, list):
            taxi_collection.insert_many(taxi_data) 
        else:
            taxi_collection.insert_one(taxi_data)
else:
    print('This place does not have enough Geodata. Please try with another city') 
               

