# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


class validateAccess:
    USER_COLLECTION = 'UserDetails'
    TAXI_COLLECTION = 'TaxiDetails'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since user name and email should be unique in users collection, this provides a way to validate user
    def validate_user(self, loginUser, email):
        key = {'name': loginUser, 'email': email, 'status': 'Active'}
        user_document = self._db.get_single_data(
            validateAccess.USER_COLLECTION, key)
        return user_document

     # Since taxi driver name, email and type of vehicle should be unique in Taxi collection, this provides a way to validate taxi
    def validate_taxi(self, loginUser, email, Type):
        key = {'name': loginUser, 'email': email, 'type': Type, 'status': 'Active'}
        taxi_document = self._db.get_single_data(
            validateAccess.TAXI_COLLECTION, key)
        return taxi_document

     # Since Taxi status and trip status need to be Active and Available respectively in order to book for a trip
    def validate_Taxi_TripStatus(self, loginUser, email, Type):
        key = {'name': loginUser, 'email': email, 'type': Type, 'status': 'Active', 'tripStatus': 'Available'}
        taxi_trip_document = self._db.get_single_data(
            validateAccess.TAXI_COLLECTION, key)
        return taxi_trip_document

