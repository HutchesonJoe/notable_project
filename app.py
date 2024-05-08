#!/usr/bin/python3
"""
Joe Hutcheson
Flask Server for Notable Project
"""
import sqlite3

from flask import Flask, g, jsonify, request

from seed_data import clients, exercises

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

def seed_clients():
  conn = g.db
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY, name,age,weight,goal)")
  cur.execute("SELECT COUNT(*) FROM clients")
  if cur.fetchone()[0] == 0:
    for c in clients:
      cur.execute("INSERT OR IGNORE INTO clients (name, age, goal, weight) VALUES (?, ?, ?, ?)", c       
    )
  conn.commit()
 
  print("Clients added.")

def seed_exercises():
  conn=g.db
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS exercises(id INTEGER PRIMARY KEY, name, category)")
  cur.execute("SELECT COUNT(*) FROM exercises")
  if cur.fetchone()[0] == 0:
    for e in exercises:
      cur.execute("INSERT OR IGNORE INTO exercises (name, category) VALUES (?, ?)", e)
  conn.commit()
  conn.close()
  print("Exercises added.")

@app.route('/')
def index():
  return """
  <h1>Welcome!</h1> 
  <h2>This Flask API is set up to accept GET, POST and DELETE request.<h2>
  <h2>GET requests for all data can be send to /{data}</h2>
  <h2>GET requests for a particular ??? can be sent to /{data}/\<id\></h2> 
  """

@app.route('/clients', methods=['GET', 'POST'])
def get_clients():
  conn=g.db
  cur=conn.cursor()
  if request.method=="GET":
    cur.execute('SELECT * FROM clients')
    clients = cur.fetchall()
    client_list=[dict(client) for client in clients]
    return jsonify(client_list)
  if request.method=="POST":
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    goal = data.get('goal')
    weight = data.get('weight')
    cur=conn.cursor()
    cur.execute("INSERT OR IGNORE INTO clients (name, age, weight, goal) VALUES (?,?,?,?)", (name, age, goal, weight))
    conn.commit()
    return "client added!"
  
@app.route('/clients/<id>', methods=['GET', 'DELETE'])
def get_client_by_id(id):
  conn=g.db
  cur=conn.cursor()
  cur.execute('SELECT * FROM clients WHERE id = ?', (id))
  client=cur.fetchone()
  if client is None:
    return jsonify({'error': 'User not found'}), 404
  if request.method=="GET":
    return jsonify(dict(client))
  if request.method=="DELETE":
    cur.execute('DELETE FROM clients WHERE id = ?', (id))
    conn.commit()
    return "client deleted!"#, jsonify(dict(client))
  
@app.route("/exercises")
def get_exercises():
  conn=g.db
  cur=conn.cursor()
  cur.execute('SELECT * FROM exercises')
  exercises=cur.fetchall()
  exercises = [dict(exercise) for exercise in exercises]
  return jsonify(exercises)

if __name__=='__main__':
  with app.app_context():
    get_db()
    seed_clients()
    seed_exercises()
  app.run(host='0.0.0.0', port=5001, debug=True)