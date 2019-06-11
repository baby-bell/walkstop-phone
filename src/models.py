from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """A user.

    See the Flask-Security_ documentation for more information.

    _Flask-Security: https://pythonhosted.org/Flask-Security/index.html
    """ 
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    roles = db.relationship("Role", secondary="roles_users",
                            backref=db.backref("users", lazy="dynamic"))


class Role(db.Model, RoleMixin):
    """User roles.

    See the Flask-Security_ documentation for more information.

    _Flask-Security: https://pythonhosted.org/Flask-Security/index.html
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.Unicode(255))


class Story(db.Model):
    """An audio story.

    The number is explicitly specified because it may be printed on some
    surface, and is used for sorting for the audio prompt.
    To ease changes, the prompt is stored as text and spoken aloud by TTS
    (text-to-speech).

    ``last_accessed`` is left as nullable because we cannot always give it a
    sensible value: newly created stories have never been accessed.
    """
    number = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    prompt = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    filename = db.Column(db.Text(), nullable=False)
    num_listens = db.Column(db.Integer(), nullable=False, default=0)
    last_accessed = db.Column(db.DateTime())

