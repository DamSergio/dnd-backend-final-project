import firebase
from config import CONFIG

firebase_app = firebase.initialize_app(CONFIG.firabase_config)
storage = firebase_app.storage()
