from flask import Flask

def create_app():
    app = Flask(__name__)

    # Initialize your extensions and register blueprints here

    return app
