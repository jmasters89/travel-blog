from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... your login logic ...
    if user and check_password_hash(user.password, password):
        login_user(user)
        # ... rest of your login success logic ...