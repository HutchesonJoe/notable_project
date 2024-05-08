#!/usr/bin/python3
"""
Joe Hutcheson
Flask Server for Notable Project
"""

from datetime import datetime

import sqlite3

from flask import Flask, g, jsonify, request

from seed_data import doctors, appointments

app=Flask(__name__)

def get_db():
  try:
    if 'db' not in g:
      g.db = sqlite3.connect('database')
      g.db.row_factory = sqlite3.Row
    return g.db
  except Exception as e:
    error_message = f"An unexpected error occured while connecting to the database: {e}"
    app.logger.error(error_message)
    return error_message, 500
  
@app.before_request
def before_request():
  g.db = get_db()

@app.teardown_request
def teardown_request(exception):
  db = g.pop('db', None)
  if db is not None:
    db.close()

def seed_doctors():
  conn = g.db
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY, first_name, last_name)")
  cur.execute("SELECT COUNT(*) FROM doctors")
  if cur.fetchone()[0] == 0:
    for d in doctors:
      cur.execute("INSERT OR IGNORE INTO doctors (first_name, last_name) VALUES (?, ?)", d       
    )
  conn.commit()
 
  print("Doctors added.")

def seed_appointments():
  conn=g.db
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY, first_name, last_name, date, time, kind, doctor_id INTEGER NOT NULL, FOREIGN KEY (doctor_id) REFERENCES doctors(id) )")
  cur.execute("SELECT COUNT(*) FROM appointments")
  if cur.fetchone()[0] == 0:
    for a in appointments:
      cur.execute("INSERT OR IGNORE INTO appointments (first_name, last_name, date, time, kind, doctor_id) VALUES (?, ?, ?, ?, ?, ?)", a)
  conn.commit()
  conn.close()
  print("Appointments added.")

@app.route('/')
def index():
  return """
  <h1>Welcome!</h1> 
  <h2>This is a Flask server that accepts HTTP requests. The README.md file provides instructions on how to send requests.</h2>
  <h2>joehutcheson@gmail.com</h2>
  """

@app.route('/doctors', methods=['GET', 'POST'])
def get_doctors():
  conn=g.db
  cur=conn.cursor()
  if request.method=="GET":
    cur.execute('SELECT * FROM doctors')
    doctors = cur.fetchall()
    doctor_list=[dict(doctor) for doctor in doctors]
    return jsonify(doctor_list)
  if request.method=="POST":
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    cur=conn.cursor()
    cur.execute("INSERT OR IGNORE INTO doctors (first_name, last_name) VALUES (?,?)", (first_name, last_name))
    conn.commit()
    return "Doctor added!"
  
@app.route('/doctors/<id>', methods=['GET', 'DELETE'])
def get_doctor_by_id(id):
  conn=g.db
  cur=conn.cursor()
  cur.execute('SELECT * FROM doctors WHERE id = ?', (id))
  doctor=cur.fetchone()
  if doctor is None:
    return jsonify({'error': 'Doctor not found'}), 404
  if request.method=="GET":
    return jsonify(dict(doctor))
  if request.method=="DELETE":
    cur.execute('DELETE FROM doctors WHERE id = ?', (id))
    conn.commit()
    return "Doctor deleted!"
  
@app.route("/appointments")
def get_appointments():
  conn=g.db
  cur=conn.cursor()
  cur.execute('SELECT * FROM appointments')
  appointments=cur.fetchall()
  appointments = [dict(appt) for appt in appointments]
  return jsonify(appointments)

@app.route("/appointments/<id>", methods = ['GET','DELETE'])
def appointment_by_id(id):
  conn=g.db
  cur=conn.cursor()
  cur.execute('SELECT * FROM appointments WHERE id = ?', (id))
  appt=cur.fetchone()
  if appt is None:
    return jsonify({'error': 'Appt not found'}), 404
  if request.method=="GET":
    return jsonify(dict(appt))
  if request.method=="DELETE":
    cur.execute('DELETE FROM appointments WHERE id = ?', (id))
    conn.commit()
    return "Appt deleted!"

@app.route("/appointments_by_doctor_and_day/<doctor_id>/<date>")
def get_appointments_by_doc_and_day(doctor_id, date):
  conn=g.db
  cur=conn.cursor()

  query = """
  SELECT * FROM appointments
  WHERE doctor_id = ? AND date = ?
  """
  cur.execute(query, (int(doctor_id), date))

  appointments = cur.fetchall()
  appointments = [dict(appt) for appt in appointments]

  if not appointments:
    return jsonify({'message': 'No appointments found for this doctor and date'}), 404

  return jsonify(appointments)

@app.route("/add_appointment", methods=["POST"])
def add_appointment():
  data = request.get_json()
  print(data)
  dr_id = data.get('doctor_id')
  date = data.get('date')
  time = data.get('time')
  conn = g.db
  cur = conn.cursor()
  cur.execute("SELECT * FROM appointments WHERE ? = doctor_id AND ? = date AND ? = time", (dr_id, date, time) )
  count = cur.fetchall()
  print(len(count))
  if time.split(":")[-1] not in ["00", "15", "30", "45"]:
    return jsonify({'error':'Appointments must be scheduled at quarters of the hour(:00, :15, :30, :45)'}), 404
  elif len(count) >= 3:
    return jsonify({'error': 'Maximum appointments scheduled for this date and time'}), 404
  else:
      first_name = data.get('first_name')
      last_name = data.get('last_name')
      kind = data.get('kind')
      #date = data.get('date')
      #time = data.get('time')
      cur=conn.cursor()
      cur.execute("INSERT OR IGNORE INTO appointments (first_name, last_name, date, time, kind, doctor_id) VALUES (?,?,?,?,?,?)", (first_name, last_name, date, time, kind, dr_id))
      conn.commit()
  return "Appt added!"

  return jsonify(appts)

if __name__=='__main__':
  with app.app_context():
    get_db()
    seed_doctors()
    seed_appointments()
  app.run(host='0.0.0.0', port=5001, debug=True)