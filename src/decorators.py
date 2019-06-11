"""\
Decorators for views that talk to the Twilio API.
"""
import flask
from flask import request, abort
from twilio.request_validator import RequestValidator


from functools import wraps


def twiml(view):
    """Attach to functions that respond to the Twilio API with TwiML.

    More information is available `in the TwiML documentation <https://www.twilio.com/docs/voice/twiml>`.
    """
    @wraps(view)
    def view_wrapper(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers["content-type"] = "text/xml"
        return response

    return view_wrapper


def validate_twilio_request(view):
    """Attach to views that act as Twilio webhooks.

    Any view with this decorator is usable only as a webhook.
    """
    @wraps(view)
    def view_wrapper(*args, **kwargs):
        validator = RequestValidator(flask.config["TWILIO_AUTH_TOKEN"])
        
        request_valid = validator.validate(request.url,
                                           request.form,
                                           request.headers.get("X-TWILIO-SIGNATURE", ""))
        if request.valid:
            return view(*args, **kwargs)
        else:
            return abort(403)

    return view_wrapper

