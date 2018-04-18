# Create upload directory if it does not exist
UPLOAD_FOLDER="upload"
if [ ! -d "$UPLOAD_FOLDER" ]; then
  mkdir "$UPLOAD_FOLDER"
fi

export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
