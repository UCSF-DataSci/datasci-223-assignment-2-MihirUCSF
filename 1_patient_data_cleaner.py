#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os

# BUG: no error handling for file not found
# FIX: added error handling for file not found
def load_patient_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
        
def clean_patient_data(patients):
    cleaned_patients = []
    
    for patient in patients:
        # BUG: typo in key 'nage' instead of 'name'
        # FIX: corrected typo 'nage' to 'name'
        patient['name'] = patient['name'].title()

        try:
            # BUG: wrong method name (fill_na vs fillna)
            # FIX: convert age to integer and handle invalid values 
        patient['age'] = int(patient['age'])
        except ValueError:
            patient['age'] = 0  # assign 0 for invalid ages
        # BUG: logic error - keeps patients under 18 instead of filtering them out
        # FIX: filter out patients under 18
        if patient['age'] < 18:
            continue
        # append cleaned patient to the list
        cleaned_patients.append(patient)
    # BUG: missing return statement for empty list
    # FIX: remove duplicates based on all patient attributes
    unique_patients = [dict(t) for t in {tuple(d.items()) for d in cleaned_patients}]
    return unique_patients

def main():
    # get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    # load patient data
    patients = load_patient_data(data_path)
    if not patients:
        # BUG: no error handling for load_patient_data failure
        # FIX: added handling for empty or failed data load
        print("No patient data loaded. Exiting.")
        return
    # clean the patient data
    cleaned_patients = clean_patient_data(patients)
    
   if cleaned_patients is None:
        # BUG: no check if cleaned_patients is None
        # FIX: added check to handle case when cleaned_patients is None
        print("No valid patient data after cleaning. Exiting.")
        return

    # print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        print(f"Name: {patient['name']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    # return the cleaned data (useful for testing)
    return cleaned_patients
if __name__ == "__main__":
    main()
