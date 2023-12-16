import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar

from .main.main import main_blueprint
from .auth.view import login_blueprint
from dotenv import load_dotenv
from .models import User, BlogPost, db
from .post.view import post_blueprint
from .utils import login_manager


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    ckeditor = CKEditor(app)
    Bootstrap5(app)

    login_manager.init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)

    app.register_blueprint(login_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(main_blueprint)
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None
                        )
    return app
