# walkstop-phone
Audio tours using Twilio

## Setup

### Dependencies
1. Install Python 3 and Docker
2. Install Pipenv with `pip install pipenv`
3. Install project dependencies with `pipenv install` (or `python -m pipenv install` if that fails)

### Services
You must have a Twilio account to test the audio interface.

### Environment Variables
Set `TWILIO_ACCOUNT_SID` to your Twilio acccount's SID, and `TWILIIO_AUTH_TOKEN` to the account's authorization token.
Connect the app to a database by setting up the `DATABASE_URL` environment variable.

## Deployment
A Dockerfile with the necessary dependencies is included.
The app must be connected to a Postgres server, as specified in `DATABASE_URL`.
