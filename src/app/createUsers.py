import random
from faker import Faker 
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.authen_DB




fake = Faker()

def create_random_users():
    users = []
    for i in range(1000000):
        username = fake.name()
        password = random.randint(0, 100)
        users.append({"username": username, "password":password})
    print('done1')
    db.authen.insert_many(users)
    
create_random_users()
print('done all')