import os

from flask import Flask, render_template
from flask_humanize import Humanize

from helpers import State, StateCssClass
from models import MonitoringStatus
from icinga2api.client import Client as Icinga2Client

app = Flask(__name__)
humanize = Humanize(app)
icinga2api = Icinga2Client(config_file='icinga2-api.ini')

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
REFRESH = 15


@app.template_filter('icinga_status')
def status_filter(value):
    try:
        return State(int(value)).name
    except ValueError:
        return 'N/A'


@app.template_filter('icinga_status_css_class')
def status_css_class_filter(value):
    try:
        return getattr(StateCssClass, State(int(value)).name).value
    except ValueError:
        return ''



@app.route('/')
def view_index():
    context = dict(
        refresh=30,
        monitoring=MonitoringStatus(apiclient=icinga2api),
        current_time = 'now'
    )
    body = render_template('index.html', **context)
    headers = dict(
        Refresh='30'
    )
    return (body, 200, headers)

if __name__ == '__main__':
    import sys

    sys.stderr.write("# This should be run using UWSGI container or `flask run` \n")
    sys.stderr.write("# FLASK_APP=main FLASK_DEBUG=1 pipenv run flask run \n")
    raise ValueError("Invalid invocation")