import time
from pymongo import MongoClient
import urllib.parse
import urllib.request
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import json
import numpy as np

DB_Name = 'CabMe'
collection = 'TaxiDetails'
db_conn = MongoClient("mongodb+srv://GLCapstone:" + urllib.parse.quote("Capstone@2022") + "@cluster0.tfzkg67.mongodb.net/test")
db = db_conn[DB_Name]
db_collection = db[collection]
db_collection_multiple = db[collection]

while True:
    try:
        taxi_details = db_collection_multiple.find({})
        for taxi_record in taxi_details:
            # Finding the Minimum, Maximum X and Y Coordinates of Taxi in the city where Taxi is registered
            polygon = ''
            with urllib.request.urlopen(
                    "https://nominatim.openstreetmap.org/search.php?q=" + taxi_record['city'] + "+" + taxi_record['country'] + "&polygon_geojson=1&format=geojson") as url:
                # with urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?q=Bangalore+India&polygon_geojson=1&format=geojson") as url:
                geoJsondata = json.load(url)
                for item in geoJsondata['features']:
                    if item['geometry']['type'] == 'Polygon' and polygon == '':
                        coordinates = item['geometry']['coordinates']
                        # print(coordinates)
                        polygon = Polygon(coordinates[0])
                        minx, miny, maxx, maxy = polygon.bounds
                        # Plot the polygon
                        xp, yp = polygon.exterior.xy
                        plt.plot(xp, yp)
                        # print(f'MinX - {minx}, MaxX - {maxx}')
                        # print(f'MinY - {miny}, MaxY - {maxy}')

            x_coordinate = taxi_record['location']['coordinates'][0] + 0.0000000001
            y_coordinate = taxi_record['location']['coordinates'][1] + 0.0000000001

            # Validation to check the incremental coordinates of Taxi doesn't go beyond the boundaries.
            # If that coordinates exceed the boundary coordinates then a random coordinate between the Min
            # and Max X and Y coordinates will be assigned to the taxi
            if maxx >= x_coordinate <= minx and maxy >= y_coordinate <= miny:
                query = {'name': taxi_record['name'], 'email': taxi_record['email']}
                update = {
                    "$set": {'location.coordinates': [x_coordinate, y_coordinate]}}
            else:
                query = {'name': taxi_record['name'], 'email': taxi_record['email']}
                update = {
                    "$set": {'location.coordinates': [np.random.uniform(minx, maxx), np.random.uniform(miny, maxy)]}}

            updated_taxi_record = db_collection.update_one(query, update)
            taxi_details = db_collection.find_one(query)
            print(taxi_details)
        time.sleep(30)
    except KeyboardInterrupt:
        break