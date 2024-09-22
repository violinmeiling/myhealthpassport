from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import DoesNotExist, ValidationError
from models import *
import certifi
import json
from flask_cors import CORS, cross_origin
import google.generativeai as genai
import os



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://violinmeiling:mathur@healthpassport.wdswq.mongodb.net/?retryWrites=true&w=majority&appName=healthpassport"
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

# Route to update a medication by ID
@app.route("/updatemedication")
def update_medication():
    try:
        userid = request.args.get('userid')
        medication_id = request.args.get('medid')
        medication_name = request.args.get('medication_name')
        intended_use = request.args.get('intended_use')
        dosage = request.args.get('dosage')
        frequency = request.args.get('frequency')
        duration = request.args.get('duration')
        user = User.objects.get(user_id=userid)

        if userid == "" or User.objects.get(user_id=userid) == None:
            return jsonify({"error": "User not found"}), 404
        if medication_id == "" or Medication.objects.get(medication_id=medication_id) == None:
            return jsonify({"error": "Medication not found"}), 404

        if medication_name !="":
            user.medications.get(medication_id=medication_id).medication_name = medication_name
        if intended_use !="":
            user.medications.get(medication_id=medication_id).intended_use = intended_use
        if dosage !="":
            user.medications.get(medication_id=medication_id).dosage = dosage
        if frequency !="":
            user.medications.get(medication_id=medication_id).frequency = frequency
        if duration !="":
            user.medications.get(medication_id=medication_id).duration = duration

        user.save()
        return jsonify({"message": "Medication updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a visit summary to a user
@app.route("/addvisit")
def add_visit_summary_to_user():
    try:
        userid = request.args.get('userid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        purpose = request.args.get('purpose')
        user = User.objects.get(user_id=userid)

        visit_summary = VisitSummary(
            date=date,
            time=time,
            clinic_name=clinic_name,
            purpose=purpose,
            medications_prescribed=[],
            diagnoses=[],
            tests_run=[]
        )

        user.visit_summaries.append(visit_summary)
        user.save()

        return jsonify({"message": "Visit summary added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to delete a visit summary by ID
@app.route("/deletevisit")
def delete_visit_summary():
    try:
        userid = request.args.get('userid')
        visit_summary_id = request.args.get('visitid') 
        user = User.objects.get(user_id=userid)
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
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a visit summary by ID
@app.route("/updatevisit")
def update_visit_summary():
    try:
        userid = request.args.get('userid')
        visit_summary_id = request.args.get('visitid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        purpose = request.args.get('purpose')

        if not userid:
            return jsonify({"error": "User ID is required"}), 400
        
        user = User.objects.get(user_id=userid)

        if userid == "" or User.objects.get(user_id=userid) == None:
            return jsonify({"error": "User not found"}), 404
        if visit_summary_id == "" or VisitSummary.objects.get(visit_summary_id=visit_summary_id) == None:
            return jsonify({"error": "Visit Summary not found"}), 404

        curr_visit_summary = user.visit_summaries.get(visit_summary_id=visit_summary_id)

        if date !="":
            curr_visit_summary.date = date
        if time !="":
            curr_visit_summary.time = time
        if clinic_name !="":
            curr_visit_summary.clinic_name = clinic_name
        if purpose !="":
            curr_visit_summary.purpose = purpose

        user.save()
        return jsonify({"message": "Visit summary updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a diagnosis to a user
@app.route("/adddiagnosis")
def add_diagnosis_to_user():
    try:
        userid = request.args.get('userid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        diagnosis_result = request.args.get('diagnosis_result')
        user = User.objects.get(user_id=userid)

        diagnosis = Diagnosis(
            date=date,
            time=time,
            clinic_name=clinic_name,
            diagnosis_result=diagnosis_result
        )

        user.diagnoses.append(diagnosis)
        user.save()

        return jsonify({"message": "Diagnosis added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to delete a diagnosis by ID
@app.route("/deletediagnosis")
def delete_diagnosis():
    try:
        userid = request.args.get('userid')
        diagnosis_id = request.args.get('diagnosisid') 
        user = User.objects.get(user_id=userid)
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
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a diagnosis by ID
@app.route("/updatediagnosis")
def update_diagnosis():
    try:
        userid = request.args.get('userid')
        diagnosis_id = request.args.get('diagnosisid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        diagnosis_result = request.args.get('diagnosis_result')
        user = User.objects.get(user_id=userid)

        if userid == "" or User.objects.get(user_id=userid) == None:
            return jsonify({"error": "User not found"}), 404
        if diagnosis_id == "" or Diagnosis.objects.get(diagnosis_id=diagnosis_id) == None:
            return jsonify({"error": "Diagnosis not found"}), 404
        
        curr_diagnosis = user.diagnoses.get(diagnosis_id=diagnosis_id)

        if date !="":
            curr_diagnosis.date = date
        if time !="":
            curr_diagnosis.time = time
        if clinic_name !="":
            curr_diagnosis.clinic_name = clinic_name
        if diagnosis_result !="":
            curr_diagnosis.diagnosis_result = diagnosis_result

        user.save()
        return jsonify({"message": "Diagnosis updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to add a past medical test to a user
@app.route("/addtest")
def add_past_medical_test_to_user():
    try:
        userid = request.args.get('userid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        test_name = request.args.get('test_name')
        user = User.objects.get(user_id=userid)

        past_medical_test = PastMedicalTest(
            date=date,
            time=time,
            clinic_name=clinic_name,
            test_name=test_name
        )

        user.past_medical_tests.append(past_medical_test)
        user.save()

        return jsonify({"message": "Past medical test added successfully!", "user": user.to_dict()}), 200

    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

# Route to delete a past medical test by ID
@app.route("/deletetest")
def delete_past_medical_test():
    try:
        userid = request.args.get('userid')
        test_id = request.args.get('testid') 
        user = User.objects.get(user_id=userid)
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
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to update a past medical test by ID
@app.route("/updatetest")
def update_past_medical_test():
    try:
        userid = request.args.get('userid')
        test_id = request.args.get('testid')
        date = request.args.get('date')
        time = request.args.get('time')
        clinic_name = request.args.get('clinic_name')
        test_name = request.args.get('test_name')
        user = User.objects.get(user_id=userid)

        if userid == "" or User.objects.get(user_id=userid) == None:
            return jsonify({"error": "User not found"}), 404
        if test_id == "" or PastMedicalTest.objects.get(test_id=test_id) == None:
            return jsonify({"error": "Past Medical Test not found"}), 404

        curr_past_medical_test = user.past_medical_tests.get(test_id=test_id)

        if date !="":
            curr_past_medical_test.date = date
        if time !="":
            curr_past_medical_test.time = time
        if clinic_name !="":
            curr_past_medical_test.clinic_name = clinic_name
        if test_name !="":
            curr_past_medical_test.test_name = test_name

        user.save()
        return jsonify({"message": "Past medical test updated successfully!", "user": user.to_dict()}), 200
    except DoesNotExist:
        return jsonify({"error": f"No user found with user_id: {userid}"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# API Route for getting Gemini response based on user input
@app.route("/api/gemini", methods=["POST"])
def get_gemini_response():
    data = request.get_json()
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"error": "Missing user_input in request body"}), 400
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input).text
    if not isinstance(response, dict):
        response = str(response)
    print(response)
    return jsonify({"response": response}), 200
    
if __name__ == "__main__": 
    app.run(debug=True)
