from flask import Flask
from setups import setup_database, setup_application
import os

if __name__ == "__main__":  
    os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)

@app.route("/")
def main():
    return "Subscription-based API"

setup_database(app)
setup_application(app)

if __name__ == "__main__":
    app.run("localhost", "8888", debug=True, use_reloader=False)