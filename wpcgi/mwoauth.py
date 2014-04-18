from wpcgi import app
from flask_mwoauth import MWOAuth
mwoauth = MWOAuth(consumer_key=app.config['CONSUMER_KEY'], consumer_secret=app.config['CONSUMER_SECRET'])