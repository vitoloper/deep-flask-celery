import os
import time
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify, send_from_directory
from celery import Celery


# Make JSON error
def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


# InvalidUsage exception
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Initialize Flask
flask_app = Flask(__name__)

# Make JSON-oriented exceptions
for code in default_exceptions:
    flask_app.register_error_handler(code, make_json_error)

# Custom exception
@flask_app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Configuration
flask_app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://',
    UPLOAD_FOLDER='upload'
)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_celery(app):
    celery = Celery(
        flask_app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['tasks']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


# Create Celery object
celery = make_celery(flask_app)


# Import tasks (after the celery object is created)
from tasks import predict as tasks_predict


# Flask routes

@flask_app.route('/predict', methods=['POST'])
def predict():
    # check if the POST request has the file part
    print(request.files)
    if 'file' not in request.files:
        raise InvalidUsage('No file part', status_code=400)
    
    file = request.files['file']
    
    # browser also submit an empty part without filename if user does not select a file
    if file.filename == '':
        raise InvalidUsage('No selected file', status_code=400)
    
    # check if file extension is allowed
    if not file or not allowed_file(file.filename):
        raise InvalidUsage('File extension not allowed', status_code=400)
    
    # save file
    filename = secure_filename(file.filename)
    f_name, f_ext = filename.rsplit('.', 1)
    timestamp = str(int(time.time()))   # seconds since Epoch
    file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], f_name + '-' + timestamp + '.' + f_ext))
    
    # TODO: long running computation intensive task here
    
    return jsonify({'status': 'GOT IT'}), 202


@flask_app.route('/status/<task_id>')
def status(task_id):
    # TODO: return task status
    return jsonify({'task_id': task_id, 'status': 'PREDICTING'})
