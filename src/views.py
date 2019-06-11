from flask import Blueprint, flash, render_template, url_for
from flask_security import login_required


from .models import db, Story


views = Blueprint("views", __name__, template_folder="templates")


@views.route("/")
@login_required
def index():
    return "Hello world"


@views.route("/manage_stories")
@login_required
def manage_stories():
    all_stories = Story.query.order_by(Story.number).all()
    return render_template("manage_stories.html", stories=all_stories)

