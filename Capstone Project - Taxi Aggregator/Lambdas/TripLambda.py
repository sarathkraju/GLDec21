from pymongo import MongoClient
import urllib.parse
import certifi
import random

ca = certifi.where()
username = urllib.parse.quote_plus('GLCapstone')
password = urllib.parse.quote_plus('Capstone@2022')
db_uri = "mongodb+srv://{}:{}@cluster0.tfzkg67.mongodb.net/test".format(username, password)
aggregator_cli = MongoClient(db_uri, tlsCAFile=ca)
database = aggregator_cli.CabMe
allUsers = database["UserDetails"]
allTaxis = database["TaxiDetails"]
allTrips = database["TripDetails"]


def lambda_handler(event, context):
    # event to start trip received
    if 'tripstatus' in event and event['tripstatus'] == 'start':
            # response trip started
            return {
                'status': 200,
                'description': 'trip started'
            }
        # event to end trip received
    if 'tripstatus' in event and event['tripstatus'] == 'end':
            # generated random number in range of 1-10 considered as trip duration
            trip_duration = random.randint(1, 10)
            # find taxi requesting to end trip
            for x in allTaxis.find():
                if event['taxiemail'] == x['email']:
                    requesting_taxi = x
                    break
            # update status of taxi as Available again
            taxi_id = requesting_taxi["_id"]
            query_update_taxi_status = {"_id": taxi_id}
            taxi_update = {
                "$set":
                    {
                        "tripStatus": "Available"
                    }
            }
            allTaxis.update_one(query_update_taxi_status, taxi_update)
            # get coordinates of taxi at end trip and update in trip table as end coordinate
            # update random number as trip duration in trip table
            end_trip_location = requesting_taxi['location']
            trip_record = allTrips.find_one({"taxiemail": requesting_taxi['email']})
            query = {"_id": trip_record["_id"]}
            trip_update = {
                "$set":
                    {
                        "endpoint": end_trip_location,
                        "duration": trip_duration
                    }
            }
            allTrips.update_one(query, trip_update)
            return {
                'status': 200,
                'description': 'trip ended'
            }
