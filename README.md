# deep-flask-celery

A deep learning (CNN) image classification web application based on Flask, Celery and the [fast.ai library](https://github.com/fastai/fastai).

## Prerequisites

You can follow the approach detailed [here](https://github.com/fastai/fastai) to install the fast.ai library.
You also need to install [flask](http://flask.pocoo.org/) and [Celery](http://www.celeryproject.org/).

In this project, Celery is configured to use [RabbitMQ](https://www.rabbitmq.com/) as the broker and [Redis](https://redis.io/) as the result backend, so you need to have both of them installed. Please refer to the documentation for further information.

## Installation, setup and run

Clone the repository and ```cd``` to the project folder:

```sh
$ git clone https://github.com/vitoloper/deep-flask-celery.git deep-flask-celery
```

Then edit the ```app.py``` file to change the configuration. You should edit the ```flask_app.config.update(...)``` part, where you can modify the following values:

* CELERY_BROKER_URL - the broker Celery will use.
* UPLOAD_FOLDER - the folder where the uploaded images will be stored.
* result_backend - where Celery will store the computation results.
* torch_model - the PyTorch model to use to make predictions.

TODO: copy the fastai library folder into the project folder. Alternatively, you can make a symbolic link to it.

Start redis and RabbitMQ (of course your setup may differ, depending on where you have installed them):

```sh
$ redis-server --daemonize yes
$ rabbitmq-server -detached
```

Activate the fastai environment and launch the two starting scripts (you may want to launch the two scripts in two separate terminal windows):

```sh
$ cd deep-flask-celery
$ source activate fastai
$ ./start-celery.sh
$ ./start-flask.sh
```

The Flask web application will start in DEBUG mode, listening on port 5000.
The Celery worker server will run the worker with a debug level of 'info'.

Finally, you can open your browser (http://localhost:5000) and submit an image for prediction.
