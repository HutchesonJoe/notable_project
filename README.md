# notable_project

## A RESTful backend using Flask and SQLite.

This application is written in __Python (Python 3.11.2)__ and uses a __Flask server__ and a __SQLite3__ database. 

- Clone this repo: `git clone https://github.com/HutchesonJoe/notable_project.git`

- Update or install Python [here](https://www.python.org/downloads/).

- From within the root directory, run `python3 -m pip install -r requirements.txt` to install the requirements.

- Run `python3 app.py` to start the server. 

- Instructions for sending HTTP requests can be found on the landing page. The server will run on `localhost:5001`.

To __get a list of all doctors__, a GET request can be sent to `localhost:5001/doctors`
- example: curl localhost:5001/doctors 
* New doctors can also be added with a POST to this URL
 - example: curl "localhost:5001/doctors" -H "Content-Type: application/json" -X POST -d '{"first_name": "Sonia", "last_name": "Nolfi"}'

To __get a list of all appointments for a particular doctor on a particular day__, a GET request can be sent to `localhost:5001/appointments_by_doctor_and_day/<doctor_id>/<date>`.
- example: curl localhost:5001/appointments_by_doctor_and_day/2/2024-05-12

To __delete an existing appointment from a doctor's calendar__, a DELETE request can be sent to `localhost:5001/appointments/<id>`.
- example: curl localhost:5001/appointments/9 -X DELETE

To __schedule a new appointment__, a POST can be sent to `localhost:5001/add_appointment`
- example: curl "localhost:5001/add_appointment" -H "Content-Type: application/json" -X POST -d '{"first_name": "Sonia", "last_name": "Nolfi", "kind": "follow-up", "date": "2024-05-12", "time": "13:45", "doctor_id": 2}'
- NOTE: Appointments must be scheduled on the __quarter of an hour__ (:00, :15, :30, :45)
- NOTE: Only __3 appointments can be scheduled on the same day and time__. 

Future devlopments goals:
- Refine database 
- More robust error handling
- Incorporate __SQLAlchemy__ for ORM (Object Relational Mapping) for future scalability