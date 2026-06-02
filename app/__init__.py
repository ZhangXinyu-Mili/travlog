import os
# This script runs automatically when our `app` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask, session, g

from app.repositories.subscription_repository import db_have_active_subscription
from app.repositories.user_repository import db_get_user_by_id

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Set the "secret key" that our app will use to sign session cookies. This can
# be anything.
#
# Anyone with access to this key can pretend to be signed in as any user. In a
# real-world project, you wouldn't store this key in your source code. To learn
# about how to manage "secrets" like this in production code, check out
# https://blog.gitguardian.com/how-to-handle-secrets-in-python/
#
# For the purpose of your assignments, you DON'T need to use any of those more
# advanced and secure methods: it's fine to store your secret key in your
# source code like we do here.
app.secret_key = 's3cr3t'

# Set up database connection.
from app import connect
from app import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname, int(connect.dbport))

# Include all modules that define our Flask route-handling functions.
from app import auth
from app import user
from app import journey
from app import event
from app import errors
from app import subscription
from app import announcement
from app import report
from app import follow
from app import helpdesk
from app import achievement

@app.before_request
def load_user():
    if "user_id" in session:
        user = db_get_user_by_id(session["user_id"])
        g.user = user

        g.premium = False
        if user["role"] in ["admin", "editor", "moderator", "supporttech"]:
            g.premium = True
        else:
            have_active_subscription = db_have_active_subscription(user["user_id"])
            if have_active_subscription:
                g.premium = True
