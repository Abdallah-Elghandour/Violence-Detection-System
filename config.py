from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    HOST = environ.get('HOST')
    PORT = environ.get("PORT")
    RESEND= environ.get("RESEND_API_KEY")
    MONGO_DB= environ.get("MONGO_DB")
    DEBUG = True