import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])

# Flask routes

@app.route('/predict', methods=['POST'])
def predict():
    # TODO: upload image, call Celery predict task
    return jsonify({'status': 'GOT IT'}), 202

@app.route('/status/<task_id>')
def status(task_id):
    # TODO: return task status
    return jsonify({'task_id': task_id, 'status': 'PREDICTING'})

if __name__ == '__main__':
    app.run(debug=True)
