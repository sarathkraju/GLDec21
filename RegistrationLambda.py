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


def lambda_handler(event, context):
    noAdd = False
    is_user_Add = False
    is_taxi_Add = False
    if "vehicleType" not in event:
        is_user_Add = True
        for x in allUsers.find():
            if event['email'] == x['email']:
                noAdd = True
                break
    else:
        is_taxi_Add = True
        for x in allTaxis.find():
            if event['email'] == x['email']:
                noAdd = True
                break

    if is_user_Add and not noAdd:
        req = dict()
        req['name'] = event['name']
        # req['userid'] = event['name'] + random.randint(0, 9)
        req['email'] = event['email']
        location = event['location']
        req['location'] = location
        allUsers.insert_one(req)
        return {
            'status': 200,
            'description': 'Record ' + event['name'] + ' added'
        }
    elif is_user_Add and noAdd:
        return {
            'status': 500,
            'description': 'user already exist'
        }

    if is_taxi_Add and not noAdd:
        req = dict()
        req['name'] = event['name']
        # req['userid'] = event['name'] + random.randint(0, 9)
        req['email'] = event['email']
        req['vehicleType'] = event['vehicleType']
        req['status'] = event['status']
        req['tripStatus'] = event['tripStatus']
        location = event['location']
        req['location'] = location
        allTaxis.insert_one(req)
        return {
            'status': 200,
            'description': 'Record ' + event['name'] + ' added'
        }
    elif is_taxi_Add and noAdd:
        return {
            'status': 500,
            'description': 'taxi already exist'
        }

