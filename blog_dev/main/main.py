from flask import render_template, Blueprint
from flask_gravatar import Gravatar
from blog_dev.models import BlogPost, db


main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@main_blueprint.route("/about")
def about():
    return render_template("about.html")


@main_blueprint.route("/contact")
def contact():
    return render_template("contact.html")

