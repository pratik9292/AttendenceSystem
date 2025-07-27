import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-fa046-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "22231161":
        {
            "name": "Jeevan Yewale",
            "major": "CSE",
            "starting_year": 2022,
            "total_attendance": 4,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "22231164":
        {
            "name": "Pratiik Deokar",
            "major": "CSE",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "22231168":
        {
            "name": "Shivraj Dhamdhare",
            "major": "CSE",
            "starting_year": 2022,
            "total_attendance": 12,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
