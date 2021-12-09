from flask.helpers import send_from_directory
from app import app
import os

host= "0.0.0.0"
if __name__ == "__main__":
    app.run(host=host , debug=True)
