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

# Route to add a visit summary to a user
@app.route("/users/<user_id>/visit_summary", methods=["POST"])
def add_visit_summary_to_user(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)

        visit_summary = VisitSummary(
            visit_summary_id=data.get("visit_summary_id"),
            date=data.get("date"),
            time=data.get("time"),
            clinic_name=data.get("clinic_name"),
            purpose=data.get("purpose")
        )

        user.visit_summaries.append(visit_summary)
        user.save()

        return jsonify({"message": "Visit summary added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to update a visit summary by ID
@app.route("/users/<user_id>/visit_summary", methods=["PUT"])
def update_visit_summary(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        visit_summary_id = data["visit_summary_id"]
        for visit_summary in user.visit_summaries:
            if visit_summary.visit_summary_id == visit_summary_id:
                if "date" in data:
                    visit_summary.date = data["date"]
                if "time" in data:
                    visit_summary.time = data["time"]
                if "clinic_name" in data:
                    visit_summary.clinic_name = data["clinic_name"]
                if "purpose" in data:
                    visit_summary.purpose = data["purpose"]
                user.save()
                return jsonify({"message": "Visit summary updated successfully!", "user": user.to_dict()}), 200

        return jsonify({"error": f"No visit summary found with visit_summary_id: {visit_summary_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to delete a visit summary by ID
@app.route("/users/<user_id>/visit_summary", methods=["DELETE"])
def delete_visit_summary(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        visit_summary = None
        visit_summary_id = data["visit_summary_id"]
        for v in user.visit_summaries:
            if v.visit_summary_id == visit_summary_id:
                visit_summary = v
                break

        if visit_summary:
            user.visit_summaries.remove(visit_summary)
            user.save()
            return jsonify({"message": "Visit summary deleted successfully!", "user": user.to_dict()}), 200
        else:
            return jsonify({"error": f"No visit summary found with visit_summary_id: {visit_summary_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a medication to a user
@app.route("/users/<user_id>/medication", methods=["POST"])
def add_medication_to_user(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)

        medication = Medication(
            medication_name=data.get("medication_name"),
            intended_use=data.get("intended_use"),
            dosage=data.get("dosage"),
            frequency=data.get("frequency"),
            duration=data.get("duration")
        )

        user.medications.append(medication)
        user.save()

        return jsonify({"message": "Medication added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a medication by ID
@app.route("/users/<user_id>/medication", methods=["PUT"])
def update_medication(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        medication_id = data["medication_id"]
        for medication in user.medications:
            if medication.medication_id == medication_id:
                if "medication_name" in data:
                    medication.medication_name = data["medication_name"]
                if "intended_use" in data:
                    medication.intended_use = data["intended_use"]
                if "dosage" in data:
                    medication.dosage = data["dosage"]
                if "frequency" in data:
                    medication.frequency = data["frequency"]
                if "duration" in data:
                    medication.duration = data["duration"]
                user.save()
                return jsonify({"message": "Medication updated successfully!", "user": user.to_dict()}), 200

        return jsonify({"error": f"No medication found with medication_id: {medication_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to delete a medication by ID
@app.route("/users/<user_id>/medication", methods=["DELETE"])
def delete_medication(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        medication = None
        medication_id = data["medication_id"]
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
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a diagnosis to a user
@app.route("/users/<user_id>/diagnosis", methods=["POST"])
def add_diagnosis_to_user(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)

        diagnosis = Diagnosis(
            date=data.get("date"),
            time=data.get("time"),
            clinic_name=data.get("clinic_name"),
            diagnosis_result=data.get("diagnosis_result")
        )

        user.diagnoses.append(diagnosis)
        user.save()

        return jsonify({"message": "Diagnosis added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a diagnosis by ID
@app.route("/users/<user_id>/diagnosis", methods=["PUT"])
def update_diagnosis(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        diagnosis_id = data["diagnosis_id"]
        for diagnosis in user.diagnoses:
            if diagnosis.diagnosis_id == diagnosis_id:
                if "date" in data:
                    diagnosis.date = data["date"]
                if "time" in data:
                    diagnosis.time = data["time"]
                if "clinic_name" in data:
                    diagnosis.clinic_name = data["clinic_name"]
                if "diagnosis_result" in data:
                    diagnosis.diagnosis_result = data["diagnosis_result"]
                user.save()
                return jsonify({"message": "Diagnosis updated successfully!", "user": user.to_dict()}), 200

        return jsonify({"error": f"No diagnosis found with diagnosis_id: {diagnosis_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to delete a diagnosis by ID
@app.route("/users/<user_id>/diagnosis", methods=["DELETE"])
def delete_diagnosis(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        diagnosis = None
        diagnosis_id = data["diagnosis_id"]
        for d in user.diagnoses:
            if d.diagnosis_id == diagnosis_id:
                diagnosis = d
                break

        if diagnosis:
            user.diagnoses.remove(diagnosis)
            user.save()
            return jsonify({"message": "Diagnosis deleted successfully!", "user": user.to_dict()}), 200
        else:
            return jsonify({"error": f"No diagnosis found with diagnosis_id: {diagnosis_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a past medical test to a user
@app.route("/users/<user_id>/past_medical_test", methods=["POST"])
def add_past_medical_test_to_user(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)

        past_medical_test = PastMedicalTest(
            date=data.get("date"),
            time=data.get("time"),
            clinic_name=data.get("clinic_name"),
            test_name=data.get("test_name")
        )

        user.past_medical_tests.append(past_medical_test)
        user.save()

        return jsonify({"message": "Past medical test added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a past medical test by ID
@app.route("/users/<user_id>/past_medical_test", methods=["PUT"])
def update_past_medical_test(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        test_id = data["test_id"]
        for test in user.past_medical_tests:
            if test.test_id == test_id:
                if "date" in data:
                    test.date = data["date"]
                if "time" in data:
                    test.time = data["time"]
                if "clinic_name" in data:
                    test.clinic_name = data["clinic_name"]
                if "test_name" in data:
                    test.test_name = data["test_name"]
                user.save()
                return jsonify({"message": "Past medical test updated successfully!", "user": user.to_dict()}), 200

        return jsonify({"error": f"No past medical test found with test_id: {test_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to delete a past medical test by ID
@app.route("/users/<user_id>/past_medical_test", methods=["DELETE"])
def delete_past_medical_test(user_id):
    try:
        data = request.get_json()
        user = User.objects.get(user_id=user_id)
        test = None
        test_id = data["test_id"]
        for t in user.past_medical_tests:
            if t.test_id == test_id:
                test = t
                break

        if test:
            user.past_medical_tests.remove(test)
            user.save()
            return jsonify({"message": "Past medical test deleted successfully!", "user": user.to_dict()}), 200
        else:
            return jsonify({"error": f"No past medical test found with test_id: {test_id}"}), 404

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {user_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500