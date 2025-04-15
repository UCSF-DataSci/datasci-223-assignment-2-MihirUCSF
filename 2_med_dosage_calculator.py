#!/usr/bin/env python3
"""
Emergency Room Medication Calculator
"""

import json
import os

# Dosage factors for different medications (mg per kg of body weight)
# These are standard dosing factors based on medical guidelines
DOSAGE_FACTORS = {
    "epinephrine": 0.01,  # Anaphylaxis
    "amiodarone": 5.00,   # Cardiac arrest
    "lorazepam": 0.05,    # Seizures
    "fentanyl": 0.001,    # Pain
    "lisinopril": 0.5,    # ACE inhibitor for blood pressure
    "metformin": 10.0,    # Diabetes medication
    "oseltamivir": 2.5,   # Antiviral for influenza
    "sumatriptan": 1.0,   # Migraine medication
    "albuterol": 0.1,     # Asthma medication
    "ibuprofen": 5.0,     # Pain/inflammation
    "sertraline": 1.5,    # Antidepressant
    "levothyroxine": 0.02 # Thyroid medication
}

# Medications that use loading doses for first administration
# BUG: missing commas between list items
# FIX: added missing commas and fixed typo 'fentynal' to 'fentanyl'
LOADING_DOSE_MEDICATIONS = [
    "amiodarone",
    "lorazepam",
    "fentanyl"
]

def load_patient_data(filepath):
    try:
        # FIX: added error handling for file not found
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # BUG: no error handling for file not found
        # FIX: log an error and return an empty list if the file is not found
        print(f"Error: File not found at {filepath}")
        return []

def calculate_dosage(patient):
    """
    Calculate medication dosage for a patient.
    """
    # Create a copy of the patient data to avoid modifying the original
    patient_with_dosage = patient.copy()
    
    # Extract patient information
    # BUG: no check if 'weight' key exists
    # FIX: added a check to ensure 'weight' is present in the patient dictionary
    if 'weight' not in patient:
        print("Error: Missing 'weight' in patient data")
        patient_with_dosage['base_dosage'] = 0
        patient_with_dosage['final_dosage'] = 0
        patient_with_dosage['warnings'] = ["Incomplete data"]
        return patient_with_dosage

    weight = patient['weight']
    
    # BUG: no check if 'medication' key exists
    # FIX: added a check to ensure 'medication' is present in the patient dictionary
    if 'medication' not in patient:
        print("Error: Missing 'medication' in patient data")
        patient_with_dosage['base_dosage'] = 0
        patient_with_dosage['final_dosage'] = 0
        patient_with_dosage['warnings'] = ["Incomplete data"]
        return patient_with_dosage

    medication = patient['medication']
    
    # Get the medication factor
    # BUG: adding 's' to medication name, which doesn't match DOSAGE_FACTORS keys
    # FIX: removed the addition of 's' to medication name
    factor = DOSAGE_FACTORS.get(medication, 0)
    
    # Calculate base dosage
    # BUG: using addition instead of multiplication
    # FIX: corrected to use multiplication for dosage calculation
    base_dosage = weight * factor
    
    # Determine if loading dose should be applied
    # BUG: no check if 'is_first_dose' key exists
    # FIX: used .get() with a default value to handle missing 'is_first_dose'
    is_first_dose = patient.get('is_first_dose', False)
    loading_dose_applied = False
    final_dosage = base_dosage
    
    # Apply loading dose if it's the first dose and the medication uses loading doses
    # BUG: incorrect condition - should check if medication is in LOADING_DOSE_MEDICATIONS
    # FIX: changed condition to check if medication is in LOADING_DOSE_MEDICATIONS
    if is_first_dose and medication in LOADING_DOSE_MEDICATIONS:
        loading_dose_applied = True
        # BUG: using addition instead of multiplication for loading dose
        # FIX: corrected to use multiplication for calculating loading dose
        final_dosage = base_dosage * 2
    
    # Add dosage information to the patient record
    patient_with_dosage['base_dosage'] = base_dosage
    patient_with_dosage['loading_dose_applied'] = loading_dose_applied
    patient_with_dosage['final_dosage'] = final_dosage
    
    # Add warnings based on medication
    warnings = []
    # BUG: typos in medication names
    # FIX: corrected typos in medication names
    if medication == "epinephrine":
        warnings.append("Monitor for arrhythmias")
    elif medication == "amiodarone":
        warnings.append("Monitor for hypotension")
    elif medication == "fentanyl":
        warnings.append("Monitor for respiratory depression")
    
    patient_with_dosage['warnings'] = warnings
    
    return patient_with_dosage

def calculate_all_dosages(patients):
    total_medication = 0
    patients_with_dosages = []
    # Process all patients
    for patient in patients:
        # Calculate dosage for this patient
        patient_with_dosage = calculate_dosage(patient)
        # Add to our list
        patients_with_dosages.append(patient_with_dosage)
        # Add to total medication
        # BUG: no check if 'final_dosage' key exists
        # FIX: added a check to ensure 'final_dosage' exists before adding to total
        total_medication += patient_with_dosage.get('final_dosage', 0)
    return patients_with_dosages, total_medication

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'meds.json')
    # BUG: no error handling for load_patient_data failure
    # FIX: handled the case where load_patient_data might return an empty list
    patients = load_patient_data(data_path)
    if not patients:
        print("No patient data available. Exiting.")
        return
    # Calculate dosages for all patients
    patients_with_dosages, total_medication = calculate_all_dosages(patients)
    # Print the dosage information
    print("Medication Dosages:")
    for patient in patients_with_dosages:
        # BUG: no check if required keys exist
        # FIX: used .get() to safely access keys in the patient dictionary
        print(f"Name: {patient.get('name', 'Unknown')}, Medication: {patient.get('medication', 'Unknown')}, "
              f"Base Dosage: {patient.get('base_dosage', 0):.2f} mg, "
              f"Final Dosage: {patient.get('final_dosage', 0):.2f} mg")
        if patient.get('loading_dose_applied'):
            print(f"  * Loading dose applied")
        if patient.get('warnings'):
            print(f"  * Warnings: {', '.join(patient.get('warnings'))}")
    
    print(f"\nTotal medication needed: {total_medication:.2f} mg")
    
    # Return the results (useful for testing)
    return patients_with_dosages, total_medication

if __name__ == "__main__":
    main()
