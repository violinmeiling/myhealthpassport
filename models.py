from flask import Flask
from mongoengine import Document, EmbeddedDocument, fields, connect
import datetime
import uuid


import uuid

class Medication(EmbeddedDocument):
    medication_id = fields.StringField(required=True, default=lambda: str(uuid.uuid4()))  # Auto-generate ID
    num_references = fields.IntField(default=0)
    medication_name = fields.StringField(required=True)
    intended_use = fields.StringField(required=True)
    dosage = fields.StringField(required=True)
    frequency = fields.StringField(required=True)
    duration = fields.StringField(required=True)

    def to_dict(self):
        return {
            "medication_id": self.medication_id,
            "medication_name": self.medication_name,
            "intended_use": self.intended_use,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "duration": self.duration
        }

class VisitSummary(EmbeddedDocument):
    visit_summary_id = fields.StringField(required=True, default=lambda: str(uuid.uuid4()))  # Auto-generate ID
    num_references = fields.IntField(default=0)
    date = fields.DateTimeField(required=True)
    time = fields.StringField(required=True)
    clinic_name = fields.StringField(required=True)
    purpose = fields.StringField(required=True)
    medications_prescribed = fields.EmbeddedDocumentListField(Medication)
    diagnoses = fields.ListField(fields.StringField())  # Store diagnosis_id
    tests_run = fields.ListField(fields.StringField())  # Store test_id

    def to_dict(self):
        return {
            "visit_summary_id": self.visit_summary_id,
            "date": self.date,
            "time": self.time,
            "clinic_name": self.clinic_name,
            "purpose": self.purpose,
            "medications_prescribed": [med.to_dict() for med in self.medications_prescribed],
            "diagnoses": self.diagnoses,
            "tests_run": self.tests_run
        }

class Diagnosis(EmbeddedDocument):
    diagnosis_id = fields.StringField(required=True, default=lambda: str(uuid.uuid4()))  # Auto-generate ID
    num_references = fields.IntField(default=0)
    date = fields.DateTimeField(required=True)
    time = fields.StringField(required=True)
    clinic_name = fields.StringField(required=True)
    diagnosis_result = fields.StringField(required=True)

    def to_dict(self):
        return {
            "diagnosis_id": self.diagnosis_id,
            "date": self.date,
            "time": self.time,
            "clinic_name": self.clinic_name,
            "diagnosis_result": self.diagnosis_result
        }

class PastMedicalTest(EmbeddedDocument):
    test_id = fields.StringField(required=True, default=lambda: str(uuid.uuid4()))  # Auto-generate ID
    num_references = fields.IntField(default=0)
    date = fields.DateTimeField(required=True)
    time = fields.StringField(required=True)
    clinic_name = fields.StringField(required=True)
    test_name = fields.StringField(required=True)

    def to_dict(self):
        return {
            "test_id": self.test_id,
            "date": self.date,
            "time": self.time,
            "clinic_name": self.clinic_name,
            "test_name": self.test_name
        }


# Main User Document
class User(Document):
    user_id = fields.StringField(required=True, unique=True)
    name = fields.StringField(required=True)
    dob = fields.StringField(required=True)
    height = fields.StringField()
    weight = fields.StringField()
    sex = fields.StringField()
    address = fields.StringField()
    insurance_provider = fields.StringField()
    insurance_policy_number = fields.StringField()
    drivers_license = fields.StringField()
    social_security_number = fields.StringField()
    
    medications = fields.EmbeddedDocumentListField(Medication)  # List of medications
    visit_summaries = fields.EmbeddedDocumentListField(VisitSummary)  # List of visit summaries
    diagnoses = fields.EmbeddedDocumentListField(Diagnosis)  # List of diagnoses
    past_medical_tests = fields.EmbeddedDocumentListField(PastMedicalTest)  # List of past medical tests

    def to_dict(self):
        return {
            "_id": str(self.id),
            "user_id": self.user_id,
            "name": self.name,
            "dob": self.dob,
            "height": self.height,
            "weight": self.weight,
            "sex": self.sex,
            "address": self.address,
            "insurance_provider": self.insurance_provider,
            "insurance_policy_number": self.insurance_policy_number,
            "drivers_license": self.drivers_license,
            "social_security_number": self.social_security_number,
            "medications": [med.to_dict() for med in self.medications],  # Assuming Medication has to_dict()
            "visit_summaries": [visit.to_dict() for visit in self.visit_summaries],
            "diagnoses": [diag.to_dict() for diag in self.diagnoses],
            "past_medical_tests": [test.to_dict() for test in self.past_medical_tests]
        }