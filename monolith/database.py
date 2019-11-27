# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    gitlab_token = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Unicode(128))
    visibility = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    gitlab_id = db.Column(db.Integer)
    ssh_url_to_repo = db.Column(db.Unicode(128))
    http_url_to_repo = db.Column(db.Unicode(128))
    web_url = db.Column(db.Unicode(128))
    name_with_namespace = db.Column(db.Unicode(128))
    path = db.Column(db.Unicode(128))
    path_with_namespace = db.Column(db.Unicode(128))
    created_at = db.Column(db.String())
    last_activity_at = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_project = relationship('User', foreign_keys='Project.user_id')


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    path = db.Column(db.Unicode(128))
    description = db.Column(db.Unicode(128))
    visibility = db.Column(db.Unicode(128))
    web_url = db.Column(db.Unicode(128))
    full_name = db.Column(db.Unicode(128))
    full_path = db.Column(db.Unicode(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_group = relationship('User', foreign_keys='Group.user_id')
