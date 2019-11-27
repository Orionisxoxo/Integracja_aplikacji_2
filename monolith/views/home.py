from flask import Blueprint, render_template

from monolith.database import db, Project
from monolith.auth import current_user


home = Blueprint('home', __name__)


@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        projects = db.session.query(Project).filter(Project.user_id == current_user.id)
    else:
        projects = None
    return render_template("index.html", projects=projects)
