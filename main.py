from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import Depends 
from propelauth_flask import init_auth, current_user
from flask import Flask 
app = Flask(__name__) 

auth = init_auth(
    "https://96933199.propelauthtest.com",
    "b795e5abc700f1a3057211d89dd481d2a6bca8f56c0da3002057c3d5bfb1b8f8aa49191e4f842b096fc9f396308b9d87"
)    
@app.route("/api/whoami")
@auth.require_user
def who_am_i():
    """This route is protected, current_user is always set"""
    return {"user_id": current_user.user_id}

if __name__ == "__main__": 
    app.run(debug=True) 

#mongosh "mongodb+srv://healthpassport.wdswq.mongodb.net/" --apiVersion 1 --username violinmeiling

uri = "mongodb+srv://violinmeiling:mathur@healthpassport.wdswq.mongodb.net/?retryWrites=true&w=majority&appName=healthpassport"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def createUser(userid, name, dob):
    db = client["healthpassport"]
    col = db["users"]
    dict = { "userid": userid, "name": name, "dob": dob }
    col.insert_one(dict)
    print("Added user " + userid + " with name " + name + " and dob " + dob)

def returnUser(userid):
    db = client["healthpassport"]
    col = db["users"]
    for x in col.find({"userid": userid}):
        print(x)

def addMedication(userid, medication, strength, frequency, duration, purpose):
    db = client["healthpassport"]
    col = db["medications"]
    dict = { "userid": userid, "medication": medication, "strength": strength, "frequency": frequency, "duration": duration, "purpose": purpose }
    col.insert_one(dict)
    print("Added medication for " + userid + " with name " + medication)

def retrieveMedications(userid):
    db = client["healthpassport"]
    col = db["medications"]
    for x in col.find({"userid": userid}):
        print(x)

def addInsurance(userid, company, policynumber):
    db = client["healthpassport"]
    col = db["insurance"]
    dict = { "userid": userid, "company": company, "policy number": policynumber}
    col.insert_one(dict)
    print("Added insurance policy for " + userid + " with company " + company)

def getInsurance(userid):
    db = client["healthpassport"]
    col = db["insurance"]
    for x in col.find({"userid": userid}):
        print(x)

