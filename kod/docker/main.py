from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
     # Läs containerns hostname
    container_id = os.uname().nodename
    return f"<h1>Hello from Docker!</h1><p>Running inside container: {container_id}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)