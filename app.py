import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery

# Initialize Flask
flask_app = Flask(__name__)

# Celery configuration
flask_app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://'
)

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

    # TODO: upload image, call Celery predict task
    tasks_predict.delay(2, 3)
    return jsonify({'status': 'GOT IT'}), 202

@flask_app.route('/status/<task_id>')
def status(task_id):
    # TODO: return task status
    return jsonify({'task_id': task_id, 'status': 'PREDICTING'})
