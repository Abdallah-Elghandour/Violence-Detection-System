from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from config import Config
from src.routes import violence_detection_route, requests_route, video_feed_route



app = Flask(__name__, template_folder='src/templates')
ma = Marshmallow(app)
api = Api(app)
violence_detection_route(api)
requests_route(api)
video_feed_route(api)


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)