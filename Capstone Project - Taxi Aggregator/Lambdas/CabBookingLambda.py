from pymongo import MongoClient
import urllib.parse
import certifi
from datetime import datetime

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
    nearest_query = dict()
    requesting_loc = dict()
    requesting_user = dict()
    for x in allUsers.find():
        if event['email'] == x['email']:
            requesting_user = x
            requesting_loc = x['location']
            nearest_query = {
                'location': {"$near": requesting_loc},
                'tripStatus' : "Available"
                }
            break

    for doc in allTaxis.find(nearest_query).limit(1):
        query = {"_id": doc["_id"]}
        trip_update = {"$set": {"tripStatus": "Unavailable"}}
        allTaxis.update_one(query, trip_update)
        trip_data = {
            'useremail': requesting_user['email'],
            'taxiemail': doc['email'],
            "startpoint": requesting_loc,
            "endpoint": "",
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "duration": 0,
            "tripstatus": ""
        }
        allTrips.insert_one(trip_data)
        return {
            'status': 200,
            'description': 'your cab is on way type ' + doc['vehicleType'] + ' Driver name ' + doc['name']
        }
        break
