from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'qwearty123qwerty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from views.posts_with_orm import postsbp
app.register_blueprint(postsbp)

from account.auth import auth
app.register_blueprint(auth)


from account.model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))