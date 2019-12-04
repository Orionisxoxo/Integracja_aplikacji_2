from flask import Blueprint, jsonify
from monolith.background import fetch_all_projects, fetch_all_groups

gitlab = Blueprint('gitlab', __name__)


@gitlab.route('/fetch/Projects')
def fetch_Projects():
    res = fetch_all_projects.delay()
    res.wait()
    return jsonify(res.result)


@gitlab.route('/fetch/Groups')
def fetch_Groups():
    res = fetch_all_groups.delay()
    res.wait()
    return jsonify(res.result)
