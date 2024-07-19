import logging
import os

from api_face_detect import create_app
from api_face_detect.util.middleware_metrics import setup_metrics

app = create_app()
setup_metrics(app)


def start():
    """
    Runs the application on a local development server.
    """
    port = int(os.environ.get('PORT', 9000))
    logging.getLogger('face_detect.main').info(f'Starting in port {port}.')
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('MODE') != 'prod',
            use_reloader=os.environ.get('MODE') != 'prod')


if __name__ == '__main__':
    start()
