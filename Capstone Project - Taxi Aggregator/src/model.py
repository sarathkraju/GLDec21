# Imports Database class from the project to provide basic functionality for database access
from datetime import date
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

# Imports validation class for user access validations 1.a and 1.b
from validation import validateAccess

# Imports MongoClient for base level access to the local MongoDB for 2
from pymongo import MongoClient

# User document contains username (String), email (String), and role (String) fields


class UserModel:
    USER_COLLECTION = 'UserDetails'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_user(self, name, email):
        user_validate = validateAccess.validate_user(self, name, email)
        if(user_validate == None):
            self._latest_error = f'User {name} does not exist'
            return -1

        key = {'name': name, 'email': email}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id

    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(
            UserModel.USER_COLLECTION, key)
        return user_document

    # Insert new User
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insertUser(self, name, email, lattitude, longitude):
        self._latest_error = ''

        user_document = self.find_user(name, email)
        if (user_document == -1):
            user_data = {'name': name, 'email': email, 'status':'Active', 'location': { 'type':'Point', 'coordinates': [lattitude,longitude] } }
            user_obj_id = self._db.insert_single_data(
            UserModel.USER_COLLECTION, user_data)
            return self.find_by_object_id(user_obj_id)
        else:
            self._latest_error = f'User {name} already exists'
            return -1

       


    # Deactivate User
    # This first validates if the user exists and then updates the status to InActive
    def inActivate(self, name, email):
        self._latest_error = ''

        user_document = self.find_user(name, email)
        if (user_document == -1):
            self._latest_error = f'Username {name} does not exists'
            return -1
        if (user_document):
            query = {'name': name, 'email': email}
            update = {
                "$set": {'status':'InActive'}}
            updated_document = self._db.update_single_data(
                UserModel.USER_COLLECTION, query, update)
            return self.__find(query)

    # Update User location at the end of the trip
    # This first validates if the user exists and then updates the location data
    def updateLocation(self, name, email, newLattitude, newLongittude):
        self._latest_error = ''

        user_document = self.find_user(name, email)
        if (user_document == -1):
            self._latest_error = f'Username {name} does not exists'
            return -1
        if (user_document):
            query = {'name': name, 'email': email}
            update = {
                "$set": {'location':{'type':'Point','coordinates':[newLattitude,newLongittude]}}}
            updated_document = self._db.update_single_data(
                UserModel.USER_COLLECTION, query, update)
            return self.__find(query)







# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class TaxiModel:
    TAXI_COLLECTION = 'TaxiDetails'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since Taxi should be unique in Taxi collection, this provides a way to fetch the Taxi document based on the Taxi name, email and Type
    def find_taxi(self, name, email, type):
        taxi_validate = validateAccess.validate_taxi(self, name, email, type)
        if(taxi_validate == None):
            self._latest_error = f'Taxi {name} of {type} type does not exist'
            return -1

        key = {'name': name, 'email': email, 'vehicleType':type}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id

    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        taxi_document = self._db.get_single_data(
            TaxiModel.TAXI_COLLECTION, key)
        return taxi_document

    # This first checks if a Taxi already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, name, email, vehicleType, lattitude, longitude):
        self._latest_error = ''

        taxi_document = self.find_taxi(name, email, vehicleType)
        if (taxi_document == -1):
            return -1
        if (taxi_document):
            self._latest_error = f'Taxi {name} already exists'
            return -1

        taxi_data = {'name': name, 'email': email, 'vehicleType': vehicleType, 'status':'Active', 'tripStatus': 'Available', 'location': { 'type':'Point', 'coordinates': [lattitude,longitude] } }
        taxi_obj_id = self._db.insert_single_data(
            TaxiModel.TAXI_COLLECTION, taxi_data)
        return self.find_by_object_id(taxi_obj_id)


    # Deactivate Taxi
    # This first validates if the Taxi exists and then updates the status to InActive
    def inActivate(self, name, email, vehicleType):
        self._latest_error = ''

        taxi_document = self.find_taxi(name, email, vehicleType)
        if (taxi_document == -1):
            self._latest_error = f'Taxi {name} of {vehicleType} type does not exists'
            return -1
        if (taxi_document):
            query = {'name': name, 'email': email, 'vehicleType' : vehicleType}
            update = {
                "$set": {'status':'InActive'}}
            updated_document = self._db.update_single_data(
                TaxiModel.TAXI_COLLECTION, query, update)
            return updated_document


