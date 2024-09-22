from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import Depends 
from propelauth_flask import init_auth, current_user, TokenVerificationMetadata
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

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
    return("Added user " + userid + " with name " + name + " and dob " + dob)

def returnUser(userid):
    db = client["healthpassport"]
    col = db["users"]
    result = []
    for x in col.find({"userid": userid}):
        result.append(x)
    return (json.dumps({"userid": result[0]['userid']}))

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

app = Flask(__name__) 
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/getmedications")
@cross_origin(origin='*')
def getmedications():
    userid = request.args.get('userid') 
    return jsonify(retrieveMedications(userid))

@app.route("/checkuserahhh")
@cross_origin(origin='*')
def checkuser():
    userid = request.args.get('userid') 
    if len(returnUser(userid)) == 0:
        return jsonify(createUser(userid, "", ""))
    else:
        return jsonify(returnUser(userid))

if __name__ == "__main__": 
    app.run(debug=True)