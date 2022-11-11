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
    # event to start trip
    # response trip started
    if 'tripstatus' in event and event['tripstatus'] == 'start':
        return {
            'status': 200,
            'description': 'trip started'
        }
    # end trip updated  event received
        # end trip updated  event received
        if 'tripstatus' in event and event['tripstatus'] == 'end':
            trip_duration = random.randint(1, 10)
            for x in allTaxis.find():
                if event['taxiemail'] == x['email']:
                    requesting_taxi = x
                    break
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
