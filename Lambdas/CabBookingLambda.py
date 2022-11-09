from pymongo import MongoClient
import urllib.parse
import certifi

ca = certifi.where()
username = urllib.parse.quote_plus('GLCapstone')
password = urllib.parse.quote_plus('Capstone@2022')
db_uri = "mongodb+srv://{}:{}@cluster0.tfzkg67.mongodb.net/test".format(username, password)
aggregator_cli = MongoClient(db_uri, tlsCAFile=ca)
database = aggregator_cli.CabMe
allUsers = database["UserDetails"]
allTaxis = database["TaxiDetails"]


def lambda_handler(event, context):
    for x in allUsers.find():
        if event['email'] == x['email']:
            requesting_user = x
            requesting_loc = x['location']
            break
    nearest_query = {'location': {"$near": requesting_loc}}
    for doc in allTaxis.find(nearest_query).limit(1):
        query = {"_id": doc["_id"]}
        trip_update = {"$set": {"tripStatus": "Unavailable"}}
        allTaxis.update_one(query, trip_update)
        return {
            'status': 200,
            'description': 'your cab is on way type ' + doc['vehicleType'] + ' Driver name ' + doc['name']
        }
        break
