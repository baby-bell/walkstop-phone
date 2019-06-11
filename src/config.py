import os


SECRET_KEY = os.environ.get("FLASK_SECRET", "TbJwCLSm5JNLGNg3DuBNr86Vk5nlxCNx")

# Twilio API parameters
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

# SQLAlchemy config
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask-security config
SECURITY_PASSWORD_SALT = os.environ.get("PASSWORD_SALT", "4ZjmX3/wiK4LuMXdAPNfEC0ou15MtGH5")


# Story audio file configuration
STORY_FILE_DIRECTORY = "story_files/"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
