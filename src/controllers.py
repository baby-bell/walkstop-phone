from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_security import login_required
from sqlalchemy.orm.exc import NoResultFound


from .models import db, Story


import logging
from pathlib import Path
import sys
import traceback


controllers = Blueprint("controllers", __name__)


@controllers.route("/stories/create", methods=["POST"])
def create_story():
    all_fields_present = True
    if "name" not in request.form or request.form["name"].strip() == "":
        flash("Please provide a name for this story.", "error")
        all_fields_present = False
    if "prompt" not in request.form or request.form["prompt"].strip() == "":
        flash("Please provide a prompt for this story.", "error")
        all_fields_present = False
    if "number" not in request.form or request.form["number"].strip() == "":
        flash("Please enter a number for this story.", "error")
        all_fields_present = False
    if "audio_file" not in request.files:
        flash("Please provide an audio file for this story.", "error")
        all_fields_present = False

    if all_fields_present:
        name, prompt, number = map(lambda f: request.form[f].strip(), ["name", "prompt", "number"])

        try:
            Story.query.filter(Story.number == int(number)).one()
            flash("Story number must be unique.", "error")
        except NoResultFound:
            audio_file = request.files["audio_file"]
            filename = number + ".mp3"
            path = str(Path(current_app.config["STORY_FILE_DIRECTORY"]) / filename)
            db.session.add(Story(number=int(number), prompt=prompt, name=name, filename=filename))
            try:
                audio_file.save(path)
                db.session.commit()
                flash("Added new story.", "success")
            except OSError as e:
                raise e
                flash("Unable to save story audio file.", "error")
                logging.error("Problem saving audio file to disk: {}".format(e))
                db.session.rollback()
            except Exception as e:
                flash("Internal server error.", "error")
                logging.error("Problem creating new story: {}".format(e))

    return redirect(url_for("views.manage_stories"))



@controllers.route("/stories/modify/<int:number>", methods=["POST"])
def modify_story(number):
    if "name" not in request.form or request.form["name"] == "":
        flash("Story name must not be blank.", "error")
    elif "prompt" not in request.form or request.form["prompt"] == "":
        flash("Story prompt must not be blank.", "error")
    else:
        try:
            story = Story.query.filter(Story.number == number).one()
            story.name = request.form["name"]
            story.prompt = request.form["prompt"]
            db.session.commit()
            flash("Saved changes.", "success")
        except NoResultFound:
            flash("No such story exists.", "error")
        except Exception as e:
            logging.error("Exception while attempting to modify story: {}".format(e))
            db.session.rollback()
            flash("Internal database error.", "error")
    return redirect(url_for("views.manage_stories"))


@controllers.route("/stories/delete/<int:number>", methods=["POST"])
def delete_story(number):
    try:
        story = Story.query.filter(Story.number == number).one()
        file_path = Path(current_app.config["STORY_FILE_DIRECTORY"]) / story.filename
        db.session.delete(story)
        db.session.commit()
        file_path.unlink()
        flash("Removed story {}".format(number), "success")
    except NoResultFound:
        flash("No story with that number exists.", "error")
    except (OSError, Exception) as e:
        flash("Internal server error.", "error")
        logging.error("Unable to delete story: {}".format(e))
    return redirect(url_for("views.manage_stories"))

