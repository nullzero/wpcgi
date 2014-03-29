from wpcgi import app

mwoauth = None

def register_mwoauth(config):
    global mwoauth
    from flask_mwoauth import MWOAuth
    mwoauth = MWOAuth(consumer_key=config.CONSUMER_KEY, consumer_secret=config.CONSUMER_SECRET)
    app.register_blueprint(mwoauth.bp)