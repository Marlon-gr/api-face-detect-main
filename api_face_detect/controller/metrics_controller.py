from flask import Blueprint, Response
from prometheus_client import (CONTENT_TYPE_LATEST, CollectorRegistry,
                               generate_latest, multiprocess)

metrics = Blueprint('metrics', __name__)


@metrics.route('/metrics')
def metrics_api():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)
