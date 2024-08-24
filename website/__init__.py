from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"  # Replace with your own secret key
    app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_starter_web_app"
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    
    mongo.init_app(app)

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Ensure User model has a find_by_id method
        return User.find_by_id(user_id)

    return app