import firebase

config = {
    "apiKey": "AIzaSyDZcAsUGY6dFE-jZvdUUqFxZ9QyFQpAStw",
    "authDomain": "dnd-app-1656b.firebaseapp.com",
    "databaseURL": "https://dnd-app-1656b-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "dnd-app-1656b",
    "storageBucket": "dnd-app-1656b.appspot.com",
    "messagingSenderId": "937003611950",
    "appId": "1:937003611950:web:40d517aaf815fb5f22ecbf",
    "measurementId": "G-9D2288S89Z",
}

firebase_app = firebase.initialize_app(config)
storage = firebase_app.storage()
