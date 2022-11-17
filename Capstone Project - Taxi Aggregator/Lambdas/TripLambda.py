from pymongo import MongoClient
import urllib.parse
import certifi
import random
import boto3

ca = certifi.where()
username = urllib.parse.quote_plus('GLCapstone')
password = urllib.parse.quote_plus('Capstone@2022')
db_uri = "mongodb+srv://{}:{}@cluster0.tfzkg67.mongodb.net/test".format(username, password)
aggregator_cli = MongoClient(db_uri, tlsCAFile=ca)
database = aggregator_cli.CabMe
allUsers = database["UserDetails"]
allTaxis = database["TaxiDetails"]
allTrips = database["TripDetails"]
AWS_REGION = 'us-east-1'
sns_client = boto3.client('sns', region_name=AWS_REGION)
AWS_REGION = 'us-east-1'
sns_client = boto3.client('sns', region_name=AWS_REGION)
topic_arn_user = "arn:aws:sns:us-east-1:374167692081:User_Notification"
topic_arn_driver = "arn:aws:sns:us-east-1:374167692081:Taxi_Driver_Notification"


def lambda_handler(event, context):
    requesting_taxi = dict()
    if 'tripstatus' in event:
        for x in allTaxis.find():
            if event['taxiemail'] == x['email']:
                requesting_taxi = x
                break
        if event['tripstatus'] == 'start':
            trip_record_start_trip_query = allTrips.find_one(
                {
                    "taxiemail": event['taxiemail'],
                    "useremail": event['useremail'],
                    "tripstatus": ""
                }
            )
            query_start_trip = {"_id": trip_record_start_trip_query["_id"]}
            trip_update_after_start = {
                "$set":
                    {
                        "tripstatus": "inprogress"
                    }
            }
            allTrips.update_one(query_start_trip, trip_update_after_start)
            sns_client.publish(
                TopicArn=topic_arn_user, 
                Message=str("Trip started"), 
                    Subject= str("Trip start confirmation")
            )
            sns_client.publish(
                TopicArn=topic_arn_driver, 
                 Message=str("Trip started"), 
                Subject= str("Trip start confirmation")
            )
            return {
                'status': 200,
                'description': 'trip started for user-' + event['useremail'] + 'by taxi-' + event['taxiemail']
            }
        elif event['tripstatus'] == 'end':
            # generated random number in range of 1-10 considered as trip duration
            trip_duration = random.randint(1, 10)
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
            trip_record = allTrips.find_one(
                {
                    "taxiemail": requesting_taxi['email'],
                    "useremail": event['useremail'],
                    "tripstatus": "inprogress"
                }
            )
            query = {"_id": trip_record["_id"]}
            # update trip data as ended only where tripstatus is inprogress
            trip_update = {
                "$set":
                    {
                        "endpoint": end_trip_location,
                        "duration": trip_duration,
                        "tripstatus": "ended"
                    }
            }
            allTrips.update_one(query, trip_update)
            sns_client.publish(
                TopicArn=topic_arn_user, 
                Message=str("Trip ended"), 
                    Subject= str("Trip end confirmation")
            )
            sns_client.publish(
                TopicArn=topic_arn_driver, 
                 Message=str("Trip ended"), 
                Subject= str("Trip end confirmation")
            )
            return {
                'status': 200,
                'description': 'trip ended for user' + event['useremail'] + 'by taxi-' + event['taxiemail']
            }
        else:
            return {
                'status': 500,
                'description': 'NO trip to start or end'
            }

