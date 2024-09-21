from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import DoesNotExist, ValidationError
from models import *
import certifi
import json


app = Flask(__name__)
#app.config['MONGO_URI'] = "mongodb+srv://minghan:minghan23@healthpassport.wdswq.mongodb.net/?retryWrites=true&w=majority&appName=healthpassport"
app.config['MONGO_URI'] = "mongodb://localhost:27017/healthpassport"
# Create a new client and connect to the server
connect(db="healthpassport", host=app.config['MONGO_URI'])

@app.route("/", methods=["GET"])
def main():
    return "Welcome to our app!"

# Route to get a user by ID
@app.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        # Query the User model for a user with the given user_id
        user = User.objects.get(user_id=user_id)
        return jsonify(user.to_dict()), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404

# Route to create a new user
@app.route("/users", methods=["POST"])
def api_create_user():
    data = request.json  # Get JSON data from the request
    # Check for required fields
    if not all(k in data for k in ("user_id", "name", "dob")):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        # Create a new User object
        user = User(
            user_id=data.get("user_id"),
            name=data.get("name"),
            dob=data.get("dob"),  # Ensure dob is a valid date in the correct format (YYYY-MM-DD)
            height=data.get("height"),
            weight=data.get("weight"),
            sex=data.get("sex"),
            address=data.get("address"),
            insurance_provider=data.get("insurance_provider"),
            insurance_policy_number=data.get("insurance_policy_number"),
            drivers_license=data.get("drivers_license"),
            social_security_number=data.get("social_security_number"),
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
@app.route("/users/<user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)

        if "name" in data:
            user.name = data["name"]
        if "dob" in data:
            user.dob = data["dob"]
        if "height" in data:
            user.height = data["height"]
        if "weight" in data:
            user.weight = data["weight"]
        if "sex" in data:
            user.sex = data["sex"]
        if "address" in data:
            user.address = data["address"]
        if "insurance_provider" in data:
            user.insurance_provider = data["insurance_provider"]
        if "insurance_policy_number" in data:
            user.insurance_policy_number = data["insurance_policy_number"]
        if "drivers_license" in data:
            user.drivers_license = data["drivers_license"]
        if "social_security_number" in data:
            user.social_security_number = data["social_security_number"]
        user.save()
        return jsonify({"message": "User updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/users/<user_id>/visit_summary", methods=["POST"])
def add_visit_summary_to_user(user_id):
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Find the user by user_id
        user = User.objects.get(user_id=user_id)

        # Helper function to find or create medications
        def find_or_create_medications(medication_data_list):
            medications = []
            for med_data in medication_data_list:
                # Check if medication already exists
                for med in user.medications:
                    if med.medication_id == med_data["medication_id"]:
                        med.num_references += 1
                        medications.append(med)
                        break
                else:
                    # Medication doesn't exist, create a new one
                    new_medication = Medication(
                        medication_id=med_data["medication_id"],
                        medication_name=med_data["medication_name"],
                        intended_use=med_data["intended_use"],
                        dosage=med_data["dosage"],
                        frequency=med_data["frequency"],
                        duration=med_data["duration"],
                        num_references=1
                    )
                    user.medications.append(new_medication)
                    medications.append(new_medication)
            return medications

        # Helper function to find or create diagnoses
        def find_or_create_diagnoses(diagnosis_data_list):
            diagnoses = []
            for diag_data in diagnosis_data_list:
                for diag in user.diagnoses:
                    if diag.diagnosis_id == diag_data["diagnosis_id"]:
                        diag.num_references += 1
                        diagnoses.append(diag)
                        break
                else:
                    # Diagnosis doesn't exist, create a new one
                    new_diagnosis = Diagnosis(
                        diagnosis_id=diag_data["diagnosis_id"],
                        date=diag_data["date"],
                        time=diag_data["time"],
                        clinic_name=diag_data["clinic_name"],
                        diagnosis_result=diag_data["diagnosis_result"],
                        num_references=1
                    )
                    user.diagnoses.append(new_diagnosis)
                    diagnoses.append(new_diagnosis)
            return diagnoses

        # Helper function to find or create past medical tests
        def find_or_create_tests(test_data_list):
            tests = []
            for test_data in test_data_list:
                for test in user.past_medical_tests:
                    if test.test_id == test_data["test_id"]:
                        test.num_references += 1
                        tests.append(test)
                        break
                else:
                    # Test doesn't exist, create a new one
                    new_test = PastMedicalTest(
                        test_id=test_data["test_id"],
                        date=test_data["date"],
                        time=test_data["time"],
                        clinic_name=test_data["clinic_name"],
                        test_name=test_data["test_name"],
                        num_references=1
                    )
                    user.past_medical_tests.append(new_test)
                    tests.append(new_test)
            return tests

        # Get medications, diagnoses, and tests from request data
        medications = find_or_create_medications(data.get("medications_prescribed", []))
        diagnoses = find_or_create_diagnoses(data.get("diagnoses", []))
        tests = find_or_create_tests(data.get("tests_run", []))

        # Create a new VisitSummary
        visit_summary = VisitSummary(
            visit_summary_id=data.get("visit_summary_id"),
            date=data.get("date"),
            time=data.get("time"),
            clinic_name=data.get("clinic_name"),
            purpose=data.get("purpose"),
            medications_prescribed=medications,
            diagnoses=[diag.diagnosis_id for diag in diagnoses],
            tests_run=[test.test_id for test in tests]
        )

        # Add the new visit summary to the user's visit summaries
        user.visit_summaries.append(visit_summary)

        # Save the updated user document
        user.save()

        return jsonify({"message": "Visit summary added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
