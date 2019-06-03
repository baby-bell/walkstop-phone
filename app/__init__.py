import flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

def create_app(test_config=None):
    app = flask.Flask("walkstop-phone")
    if test_config is None:
        app.config.from_pyfile("config.py", silent=False)
    else:
        app.config.from_mapping(test_config)

    csrf = CSRFProtect(app)
    from .views import views
    from .controllers import controllers
    from .phone_interface import webhooks
    app.register_blueprint(views)
    app.register_blueprint(controllers, url_prefix="/api")
    app.register_blueprint(webhooks, url_prefix="/voice")
    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)
    from .login import security, user_datastore
    security.init_app(app, user_datastore)
    return app

app = create_app()
