from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    roles = db.relationship("Role", secondary="roles_users",
                            backref=db.backref("users", lazy="dynamic"))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.Unicode(255))


class Story(db.Model):
    number = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    prompt = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    filename = db.Column(db.Text(), nullable=False)

