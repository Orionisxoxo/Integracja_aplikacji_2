from flask import Blueprint, jsonify
from monolith.background import fetch_all_projects


gitlab = Blueprint('gitlab', __name__)


@gitlab.route('/fetch')
def fetch_runs():
    res = fetch_all_projects.delay()
    res.wait()
    return jsonify(res.result)
