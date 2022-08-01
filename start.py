from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'qwearty123qwerty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)

# from views.posts import posts_bp
# app.register_blueprint(posts_bp)


if __name__ == '__main__':
    from views.posts_with_orm import postsbp

    app.register_blueprint(postsbp)
    app.run(port=8000)
