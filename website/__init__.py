from flask import Flask
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"  # Replace with your own secret key
    
    # Ensure the upload folder exists
    if not os.path.exists(app.root_path, 'static/uploads'):
        os.makedirs(app.root_path, 'static/uploads')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Update this line

    @login_manager.user_loader
    def load_user(user_id):
        # Ensure User model has a find_by_id method
        return User.find_by_id(user_id)

    return app
