#!/usr/bin/python3
"""
Joe Hutcheson
Flask Server for Notable Project
"""
import sqlite3

from flask import Flask
from flask import request
from flask import jsonify

from seed_data import clients, exercises

app=Flask(__name__)

def run_db():
  conn=sqlite3.connect('client.db')
  conn.row_factory=sqlite3.Row
  conn.commit()
  print("Database created.")
  return conn

def seed_clients():
  conn=run_db()
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
  conn=run_db()
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS exercises(id INTEGER PRIMARY KEY, name, category)")
  cur.execute("SELECT COUNT(*) FROM exercises")
  if cur.fetchone()[0] == 0:
    for e in exercises:
      cur.execute("INSERT OR IGNORE INTO exercises (name, category) VALUES (?, ?)", e)
  conn.commit()
  print("Exercises added.")

@app.route('/clients', methods=['GET', 'POST'])
def get_clients():
  conn=run_db()
  cur=conn.cursor()
  if request.method=="GET":
    cur.execute('SELECT * FROM clients')
    clients = cur.fetchall()
    conn.close()
  
    client_list=[dict(client) for client in clients]
    return jsonify(client_list)
  if request.method=="POST":
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    goal = data.get('goal')
    weight = data.get('goal')
    conn=sqlite3.connect('client.db')
    cur=conn.cursor()
    cur.execute("INSERT OR IGNORE INTO clients (name, age, weight, goal) VALUES (?,?,?,?)", (name, age, goal, weight))
    conn.commit()
    return "client added!"
  
@app.route('/clients/<id>', methods=['GET', 'DELETE'])
def get_client_by_id(id):
  conn=run_db()
  cur=conn.cursor()
  cur.execute('SELECT * FROM clients WHERE id = ?', (id))
  client=cur.fetchone()
  if client is None:
    return jsonify({'error': 'User not found'}), 404
  if request.method=="GET":
    return jsonify(dict(client))
    conn.close()
  if request.method=="DELETE":
    cur.execute('DELETE FROM clients WHERE id = ?', (id))
    conn.commit()
    conn.close()
    return "client deleted!"



if __name__=='__main__':
  run_db()
  #fetch_all()
  seed_clients()
  seed_exercises()
  app.run(host='0.0.0.0', port=5001, debug=True)