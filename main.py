from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector

app = FastAPI(title="Clinic Booking System API")

# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="clinic_db"
    )

# --- Models ---
class Patient(BaseModel):
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    date_of_birth: Optional[str]

class Doctor(BaseModel):
    full_name: str
    specialization: Optional[str]
    email: Optional[str]
    phone: Optional[str]

# --- Patients CRUD ---
@app.post("/patients")
def create_patient(p: Patient):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("INSERT INTO Patients (full_name, email, phone, date_of_birth) VALUES (%s,%s,%s,%s)",
                (p.full_name, p.email, p.phone, p.date_of_birth))
    db.commit()
    cur.close()
    db.close()
    return {"message": "Patient added successfully"}

@app.get("/patients")
def get_patients():
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Patients")
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, p: Patient):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("UPDATE Patients SET full_name=%s, email=%s, phone=%s, date_of_birth=%s WHERE patient_id=%s",
                (p.full_name, p.email, p.phone, p.date_of_birth, patient_id))
    db.commit()
    cur.close()
    db.close()
    return {"message": "Patient updated"}

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM Patients WHERE patient_id=%s", (patient_id,))
    db.commit()
    cur.close()
    db.close()
    return {"message": "Patient deleted"}

# --- Doctors CRUD ---
@app.post("/doctors")
def create_doctor(d: Doctor):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("INSERT INTO Doctors (full_name, specialization, email, phone) VALUES (%s,%s,%s,%s)",
                (d.full_name, d.specialization, d.email, d.phone))
    db.commit()
    cur.close()
    db.close()
    return {"message": "Doctor added successfully"}

@app.get("/doctors")
def get_doctors():
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Doctors")
    data = cur.fetchall()
    cur.close()
    db.close()
    return data
