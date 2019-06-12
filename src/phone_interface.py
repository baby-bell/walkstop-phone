"""\
Webhooks for the Twilio API, used in the audio interface.
"""

from flask import abort, Blueprint, current_app, request, send_file, url_for
from twilio.twiml.voice_response import Gather, VoiceResponse
from sqlalchemy.orm.exc import NoResultFound


from .decorators import twiml, validate_twilio_request
from .models import db, Story


from datetime import datetime
import logging
from pathlib import Path


webhooks = Blueprint('twilio', __name__)


@webhooks.route("/welcome", methods=["POST"])
@validate_twilio_request
@twiml
def welcome():
    """Respond to incoming calls.

    Prompts for a story number.
    """
    response = VoiceResponse()
    with response.gather(action=url_for("twilio.play_story"), method="POST") as g:
        g.say(message="""
Welcome to WalkStops Haight and Fillmore Oral History Corner. 

If you know which story you would like to hear, press the number now. If you are not sure, please listen to the different oral histories and make your choice at any time by pressing the number that corresponds to the story.
""")
        g.pause()
        all_stories = Story.query.order_by(Story.number).all()
        for story in all_stories:
            g.say("To hear {}, press {}".format(story.prompt, story.number))

    response.redirect(url_for("twilio.goodbye"))
    return response



@webhooks.route("/play_story", methods=["POST"])
@validate_twilio_request
@twiml
def play_story():
    """\
    Play a story for the user.
    """
    story_number = int(request.form["Digits"])
    response = VoiceResponse()
    try:
        Story.query.filter(Story.number == story_number).one()
    except NoResultFound:
        response.say("I could not find story number {}. Please try another number.".format(request.form["Digits"]))
        response.redirect(url_for("twilio.welcome"))
        return response

    response.play(url_for("twilio.get_story_audio", story_number=story_number))
    response.redirect(url_for("twilio.goodbye"))
    return response


@webhooks.route("/get_story_audio/<int:story_number>.mp3")
@validate_twilio_request
def get_story_audio(story_number):
    """\
    Fetch the audio file for a particular story.
    """
    try:
        story = Story.query.filter(Story.number == story_number).one()
        story.num_listens += 1
        story.last_accessed = datetime.utcnow()
        db.session.commit()
    except NoResultFound:
        logging.warning("User requested nonexistent story number {}".format(story_number))
        return abort(404)

    story_dir = Path(current_app.config["STORY_FILE_DIRECTORY"])
    try:
        story_file = open(story_dir/story.filename, "rb")
        logging.info("User requested story {}".format(story_file))
        return send_file(story_file, mimetype="audio/mpeg")
    except OSError as e:
        logging.error("Could not retrieve file for story '{}'. \nException: {}".format(story.name,
                                                                                       e))
        return abort(500)


@webhooks.route("/goodbye", methods=["POST"])
@validate_twilio_request
@twiml
def goodbye():
    """\
    Thank the user and hang up the phone.

    This should be triggered if the user spends too much time without
    any input.
    """
    response = VoiceResponse()
    response.say("Thank you for participating in WalkStops Haight and Fillmore Oral History Corner." +
                 "Good bye.")
    response.hangup()

    return response

