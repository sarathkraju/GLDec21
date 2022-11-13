import json
import urllib.parse
# Imports datetime class to create timestamp for weather data storage
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from bson.son import SON
# Imports MongoClient and GEOSPHERE for base level access to the local MongoDB and geospatial data
from pymongo import GEOSPHERE, MongoClient
from shapely.geometry import Point, Polygon

print('############### CAPSTONE PROJECT ####################')
print('')
print('### RUNNING SETUP ###')
print('')
# getting country and city from client for setting boundary
country = input('please enter country for setting up CabMe App: ')
print('')
city = input('please enter city for setting up CabMe App: ')
print('')
polygon=''
print('### SETTING BOUNDARY ###')
# with urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?q=Bangalore+India&polygon_geojson=1&format=geojson") as url:
with urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?q="+ city +"+"+country+"&polygon_geojson=1&format=geojson") as url:
    geoJsondata = json.load(url)
    for item in geoJsondata['features']:
        if(item['geometry']['type'] == 'Polygon' and polygon==''):
           coordinates = item['geometry']['coordinates']
           print(coordinates)
           polygon = Polygon(coordinates[0])           
           minx, miny, maxx, maxy = polygon.bounds
           # Plot the polygon
           xp,yp = polygon.exterior.xy           
           plt.plot(xp,yp)


if polygon!='':
    print('### BOUNDARY SET - PLEASE VERIFY POP UP WINDOW ###')
    RELATIVE_CONFIG_PATH = 'C:/Users/sarat/OneDrive/Documents/ACSE_IITM_GreatLearning/Capstone Project - Taxi Aggregator/config/'
    POINTS = []
    DB_NAME = 'CabMe'
    USER_COLLECTION = 'UserDetails'
    TAXI_COLLECTION = 'TaxiDetails'
    TRIP_COLLECTION = 'TripDetails'

    print('### Connecting to MongoDB ###')
    print('')
    # This will initiate connection to the mongodb
    db_handle = MongoClient("mongodb+srv://GLCapstone:"  + urllib.parse.quote("Capstone@2022") + "@cluster0.tfzkg67.mongodb.net/test")

    # We drop the existing database including all the collections and data
    db_handle.drop_database(DB_NAME)

    # We recreate the database with the same name
    cabMe_dbh = db_handle[DB_NAME]

    print('### Connected to MongoDB ###')
    print('')
    print('### Loading User Data to UserDetails collection ###')
    print('')
  
    
    # user data import
    # User document includes name, email and location
    # Reads UserDetails.json and loads them to user_collection
    with open(RELATIVE_CONFIG_PATH+USER_COLLECTION+'.json') as user_fh:
        # This loads the json file to user_data
        user_data = json.load(user_fh)
        
        while len(POINTS) < len(user_data) :
            pnt = Point(np.random.uniform(minx, maxx) , np.random.uniform(miny, maxy))                
            if polygon.contains(pnt):            
                POINTS.append(pnt)

        for user,point in zip(user_data,POINTS):   
            user['location']['coordinates'][0] = point.x
            user['location']['coordinates'][1] = point.y
            user['country'] = country
            user['city'] = city
            user['Timestamp'] = datetime.now()
            POINTS=[]        

        # Plot the polygon
        xp,yp = polygon.exterior.xy
        plt.plot(xp,yp)

        # Plot the list of points
        xs = [point.x for point in POINTS]
        ys = [point.y for point in POINTS]
        plt.scatter(xs, ys,color="red")
        plt.show() 
                   
        # This creates and return a pointer to the users collection
        user_collection = cabMe_dbh[USER_COLLECTION]
        # Create Index(es)
        user_collection.create_index([('location', GEOSPHERE)])
        # This inserts the data item as a document in the user collection
        if isinstance(user_data, list):
            user_collection.insert_many(user_data) 
        else:
            user_collection.insert_one(user_data)
    
    print('### User data loaded successfully ###')
    print('')
    print('### Loading Taxi Data to UserDetails collection ###')
    print('')
       
    # Taxi data import
    # User document includes name, email, location and Type
    # Reads TaxiDetails.json and loads them to taxi_collection
    with open(RELATIVE_CONFIG_PATH+TAXI_COLLECTION+'.json') as taxi_fh:
        # This loads the json file to user_data
        taxi_data = json.load(taxi_fh)
        
        while len(POINTS) < len(taxi_data)*20 :
            pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            if polygon.contains(pnt):            
                POINTS.append(pnt)

        POINTS = POINTS[0::20]
        for taxi,point in zip(taxi_data,POINTS):           
            taxi['location']['coordinates'][0] = point.x
            taxi['location']['coordinates'][1] = point.y
            taxi['country'] = country
            taxi['city'] = city
            taxi['Timestamp'] = datetime.now()
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
        print('### Taxi data loaded successfully ###')
        print('')

    # This creates and return a pointer to the users collection
    trip_collection = cabMe_dbh[TRIP_COLLECTION]
else:
    print('This place does not have enough Geodata. Please try with another city') 
               

# # simulator code for incrementing the taxi coordinates slowly
# # if incrementing spatial condition doesnt contain inside polygon boundary then randomly assign coordinates
# #timer need to be added for the script to run at certain interval
# newPoint = []
# for taxi in taxi_collection.find({"status": "Active"}):
#     _id= taxi["_id"]
#     xPoint = taxi['location']['coordinates'][0] + (maxx-minx)/10000
#     yPoint = taxi['location']['coordinates'][1] + (maxy-miny)/10000
#     if polygon.contains(pnt):            
#         newPoint.append(pnt)
#     else:
#         while len(newPoint) < len(taxi_data)*20 :
#             pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
#             if polygon.contains(pnt):            
#                 newPoint.append(pnt)
    
#     taxi['location']['coordinates'][0] = point.x
#     taxi['location']['coordinates'][1] = point.y

#     taxi_collection.update_one({"_id":_id}, {"$set":{"coordinates":[point.x, point.y]}})
#     newPoint = []

