from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import DoesNotExist, ValidationError
from models import *
import certifi
import json
from flask_cors import CORS, cross_origin



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
# Create a new client and connect to the server
connect(db="healthpassport", host=app.config['MONGO_URI'])

@app.route("/", methods=["GET"])
@cross_origin(origin='*')
def main():
    return "Welcome to our app!"

# Route to get a user by ID
@app.route("/users", methods=["GET"])
@cross_origin(origin='*')
def get_user_by_id():
    userid = request.args.get('userid') 
    try:
        # Query the User model for a user with the given user_id
        user = User.objects.get(user_id=userid)
        return jsonify(user.to_dict()), 200
    except DoesNotExist:
        api_create_user(userid)
        return jsonify("created new user")

def api_create_user(userid):
    #data = request.json  # Get JSON data from the request
    # Check for required fields
    #if not all(k in data for k in ("user_id", "name", "dob")):
        #return jsonify({"error": "Missing required fields"}), 400
    try:
        # Create a new User object
        user = User(
            user_id=userid,
            name="",
            dob="1900-01-01",  # Ensure dob is a valid date in the correct format (YYYY-MM-DD)
            height="",
            weight="",
            sex="",
            address="",
            insurance_provider="",
            insurance_policy_number="",
            drivers_license="",
            social_security_number="",
            medications=[],  # Empty list for now, you can add medications separately later
            visit_summaries=[],
            diagnoses=[],
            past_medical_tests=[]
        )
        user.save()
        return jsonify({"message": "User created successfully!", "user": user.to_json()}), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the user"}), 500

# Route to update a user by ID
@app.route("/updateuser")
def update_user_by_id():
    try:
        userid = request.args.get('userid') 
        name = request.args.get('name')
        dob = request.args.get('dob') 
        height = request.args.get('height')
        weight = request.args.get('weight') 
        sex = request.args.get('sex')
        address = request.args.get('address') 
        insurance_provider = request.args.get('provider')
        insurance_policy = request.args.get('policy') 
        drivers_license = request.args.get('dlnum')
        ssn = request.args.get('ssn') 
        user = User.objects.get(user_id=userid)

        if name != "":
            user.name = name
        if dob != "":
            user.dob = dob
        if height != "":
            user.height = height
        if weight != "":
            user.weight = weight
        if sex != "":
            user.sex = sex
        if address != "":
            user.address = address
        if insurance_provider != "":
            user.insurance_provider = insurance_provider
        if insurance_policy != "":
            user.insurance_policy_number = insurance_policy
        if drivers_license != "":
            user.drivers_license = drivers_license
        if ssn != "":
            user.social_security_number = ssn
        user.save()
        return jsonify({"message": "User updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to add a medication to a user
@app.route("/addmedication")
def add_medication_to_user():
    try:
        userid = request.args.get('userid')
        medname = request.args.get('medname') 
        intendeduse = request.args.get('use') 
        dosage = request.args.get('dosage') 
        frequency = request.args.get('frequency') 
        duration = request.args.get('duration') 
        user = User.objects.get(user_id=userid)

        medication = Medication(
            medication_name=medname,
            intended_use=intendeduse,
            dosage=dosage,
            frequency=frequency,
            duration=duration
        )

        user.medications.append(medication)
        user.save()

        return jsonify({"message": "Medication added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to delete a medication by ID
@app.route("/deletemedication")
def delete_medication():
    try:
        userid = request.args.get('userid')
        medication_id = request.args.get('medid') 
        user = User.objects.get(user_id=userid)
        for m in user.medications:
            if m.medication_id == medication_id:
                medication = m
                break

        if medication:
            user.medications.remove(medication)
            user.save()
            return jsonify({"message": "Medication deleted successfully!", "user": user.to_dict()}), 200
        else:
            return jsonify({"error": f"No medication found with medication_id: {medication_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    
if __name__ == "__main__": 
    app.run(debug=True)
