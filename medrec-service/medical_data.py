SAMPLE_RECORDS = [
    {
        "patient_id": "P001",
        "name": "John Smith",
        "age": 45,
        "diagnosis": "Hypertension",
        "treatment": "Lisinopril 10mg daily",
        "doctor": "Dr. Sarah Johnson",
        "date": "2024-11-08",
        "notes": "Blood pressure well controlled. Continue current medication.",
        "vitals": {
            "blood_pressure": "128/82",
            "heart_rate": 72,
            "temperature": 98.6
        }
    },
    {
        "patient_id": "P002", 
        "name": "Emily Davis",
        "age": 32,
        "diagnosis": "Type 2 Diabetes",
        "treatment": "Metformin 500mg twice daily",
        "doctor": "Dr. Michael Chen",
        "date": "2024-11-07",
        "notes": "HbA1c improved to 7.2%. Patient responding well to treatment.",
        "vitals": {
            "blood_pressure": "118/76",
            "heart_rate": 68,
            "glucose": 142
        }
    },
    {
        "patient_id": "P003",
        "name": "Robert Wilson",
        "age": 67,
        "diagnosis": "Coronary Artery Disease",
        "treatment": "Atorvastatin 40mg, Aspirin 81mg",
        "doctor": "Dr. Lisa Rodriguez",
        "date": "2024-11-06",
        "notes": "Recent cardiac catheterization shows stable disease. Continue medications.",
        "vitals": {
            "blood_pressure": "132/86",
            "heart_rate": 78,
            "cholesterol": 185
        }
    },
    {
        "patient_id": "P004",
        "name": "Maria Garcia",
        "age": 28,
        "diagnosis": "Asthma",
        "treatment": "Albuterol inhaler PRN, Fluticasone daily",
        "doctor": "Dr. James Williams",
        "date": "2024-11-05",
        "notes": "Asthma well controlled with current regimen. No recent exacerbations.",
        "vitals": {
            "blood_pressure": "115/72",
            "heart_rate": 64,
            "oxygen_saturation": 98
        }
    },
    {
        "patient_id": "P005",
        "name": "David Lee",
        "age": 55,
        "diagnosis": "Chronic Kidney Disease Stage 3",
        "treatment": "ACE inhibitor, Phosphate binders",
        "doctor": "Dr. Patricia Brown",
        "date": "2024-11-04",
        "notes": "eGFR stable at 45. Continue nephroprotective therapy.",
        "vitals": {
            "blood_pressure": "135/88",
            "heart_rate": 76,
            "creatinine": 1.8
        }
    }
]

def get_patient_record(patient_id):
    for record in SAMPLE_RECORDS:
        if record["patient_id"] == patient_id:
            return record
    return None

def get_all_records():
    return SAMPLE_RECORDS

def search_records(query):
    query = query.lower()
    results = []
    for record in SAMPLE_RECORDS:
        if (query in record["name"].lower() or 
            query in record["patient_id"].lower() or
            query in record["diagnosis"].lower()):
            results.append(record)
    return results