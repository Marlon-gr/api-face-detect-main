from flask import Blueprint

start_route = Blueprint('start_route', __name__)


@start_route.route('/')
def welcome():
    return 'Welcome to Face Detect API, read documentation in /docs ' \
           'for further questions.', 200


@start_route.route('/health')
def health():
    """Endpoint used for know if the API is stand up"""
    return "up", 200
