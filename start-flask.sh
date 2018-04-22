# Create upload directory if it does not exist
UPLOAD_FOLDER="upload"
if [ ! -d "$UPLOAD_FOLDER" ]; then
  mkdir "$UPLOAD_FOLDER"
fi

export FLASK_APP=app.py
export FLASK_DEBUG=1

# You may want to bind to host 0.0.0.0 (e.g. if you build a Docker image or need full access)
flask run
# flask run --host=0.0.0.0
