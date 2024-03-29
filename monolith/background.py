from celery import Celery
from monolith.database import db, User, Project, Group
import gitlab

BACKEND = BROKER = 'redis://212.182.24.105:32768'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def fetch_all_projects():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    projects_fetched = {}

    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.gitlab_token is None:
                continue
            print('Fetching Gitlab Projects for %s' % user.email)
            projects_fetched[user.id] = fetch_projects(user)

    return projects_fetched


def project2db(user, user_project):
    """Used by fetch_projects to convert a Gitlab user project into a DB entry.
    """
    project = Project()
    project.user_project = user
    project.gitlab_id = user_project.id
    project.name = user_project.name
    project.description = user_project.description
    project.visibility = user_project.visibility
    project.ssh_url_to_repo = user_project.ssh_url_to_repo
    project.http_url_to_repo = user_project.http_url_to_repo
    project.web_url = user_project.web_url
    project.name_with_namespace = user_project.name_with_namespace
    project.path = user_project.path
    project.path_with_namespace = user_project.path_with_namespace
    project.created_at = user_project.created_at
    project.last_activity_at = user_project.last_activity_at

    return project


def fetch_projects(user):
    gl = gitlab.Gitlab('https://umcs.schneiderp.ovh', private_token=user.gitlab_token)
    projects = 0

    all_projects = gl.projects.list(all=True)
    for project in all_projects:
        q = db.session.query(Project).filter(Project.gitlab_id == project.id)
        one_project = q.first()

        if one_project is None:
            db.session.add(project2db(user, project))
            projects += 1

    db.session.commit()
    return projects


@celery.task
def fetch_all_groups():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    groups_fetched = {}

    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.gitlab_token is None:
                continue
            print('Fetching Gitlab Groups for %s' % user.email)
            groups_fetched[user.id] = fetch_groups(user)

    return groups_fetched


def group2db(user, user_group):
    """Used by fetch_projects to convert a Gitlab user project into a DB entry.
    """
    group = Group()
    group.user_group = user
    group.gitlab_id = user_group.id
    group.name = user_group.name
    group.description = user_group.description
    group.visibility = user_group.visibility
    group.ssh_url_to_repo = user_group.ssh_url_to_repo
    group.http_url_to_repo = user_group.http_url_to_repo
    group.web_url = user_group.web_url
    group.name_with_namespace = user_group.name_with_namespace
    group.path = user_group.path
    group.path_with_namespace = user_group.path_with_namespace
    group.created_at = user_group.created_at
    group.last_activity_at = user_group.last_activity_at

    return group


def fetch_groups(user):
    gl = gitlab.Gitlab('https://umcs.schneiderp.ovh', private_token=user.gitlab_token)
    groups = 0

    all_groups = gl.groups.list(all=True)
    for group in all_groups:
        q = db.session.query(Group).filter(Group.gitlab_id == group.id)
        one_group = q.first()

        if one_group is None:
            db.session.add(group2db(user, group))
            groups += 1

    db.session.commit()
    return groups

