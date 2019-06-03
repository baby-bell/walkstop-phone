#!/bin/bash
export FLASK_APP=app/
export FLASK_DEBUG=true
source twilio.env
flask run
