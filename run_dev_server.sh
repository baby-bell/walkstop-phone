#!/bin/bash
export FLASK_APP=src
export FLASK_DEBUG=true
source twilio.env
flask run
