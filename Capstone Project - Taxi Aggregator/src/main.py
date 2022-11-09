from model import UserModel, TaxiModel
from datetime import datetime

print('############### CAPSTONE PROJECT ####################')
print('')
print('## User Details ##')
print('')
print(f'## Case 1. To verfiy if user exists or registered')
print('')
# getting input from client for loginUser
userName = input('please enter login user name for accessing CabMe: ')
print('')
userEmail = input('please enter login email for accessing CabMe: ')
print('')
user_coll = UserModel()
user_document = user_coll.find_user(userName, userEmail)
if (user_document == -1):
    print(f'Failure! Error: {user_coll.latest_error}')
else:
    print(f'Success! Search output: {user_document}')

print('')
print(f'## Case 2: inserting new User. inserting hardcoded user details ')
user_document = user_coll.insertUser(
    'Sarath', 'sarath@example.com', 28.12434, 77.3456)
if (user_document == -1):
    print(f'Failure! Error: {user_coll.latest_error}')
else:
    print(f'Successfully inserted new user. Output: {user_document}')

print('')
print(f'## Case 3: Validate duplicate user insert in User model')
user_document = user_coll.insertUser(
    'Sarath', 'sarath@example.com', 28.12434, 77.34567)
if (user_document == -1):
    print(f'Failure! Error: {user_coll.latest_error}')
else:
    print(f'Successfully inserted duplicate user. Output: {user_document}')

print('')
print(f'## Case 4: Inactivate User')
user_document = user_coll.inActivate('Sarath', 'sarath@example.com')
if (user_document == -1):
    print(f'Failure! Error: {user_coll.latest_error}')
else:
    print(f'Successfully InActivated user. Output: {user_document}')

print('')
print(f'## Case 5: Update location of User')
user_document = user_coll.updateLocation('Mohan', 'Mohan.P@unknownmail.com',28.12434, 77.34567)
if (user_document == -1):
    print(f'Failure! Error: {user_coll.latest_error}')
else:
    print(f'Successfully updated location of user. Output: {user_document}')

print('')
print('## Taxi Details ##')
print('')

print(f'## Case 6: To verify if Taxi exists')
print('')
