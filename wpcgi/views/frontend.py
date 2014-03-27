#!/data/project/nullzerobot/python/bin/python

from p_flask import (Blueprint, render, request,
                   flash, url_for, redirect, session, abort)
from decorators import langswitch
from wpcgi import tools, app
from flask_oauth import OAuth, OAuthRemoteApp, parse_response, OAuthException
import flask_oauth, json

frontend = Blueprint('frontend', __name__)

class MWOAuthRemoteApp(OAuthRemoteApp):
    def handle_oauth1_response(self):
        """Handles an oauth1 authorization response.  The return value of
        this method is forwarded as first argument to the handling view
        function.
        """
        client = self.make_client()
        resp, content = client.request('%s&oauth_verifier=%s' % (
            self.expand_url(self.access_token_url),
            request.args['oauth_verifier'],
        ), self.access_token_method)
        print resp, content
        data = parse_response(resp, content)
        if not self.status_okay(resp):
            raise OAuthException('Invalid response from ' + self.name,
                                 type='invalid_response', data=data)
        return data

oauth = OAuth()

base_url = 'https://www.mediawiki.org/w/index.php'
mwoauth = MWOAuthRemoteApp(oauth, 'mw.org',
    base_url = base_url,
    request_token_url=base_url,
    request_token_params = {'title': 'Special:MWOAuth/initiate',
                            'oauth_callback': 'oob'},
    access_token_url=base_url + "?title=Special:MWOAuth/token",
    authorize_url='https://www.mediawiki.org/wiki/Special:MWOAuth/authorize',
    consumer_key=app.config['CONSUMER_KEY'],
    consumer_secret=app.config['CONSUMER_SECRET'],
)
oauth.remote_apps['mw.org'] = mwoauth

@mwoauth.tokengetter
def get_mwo_token(token=None):
    return session.get('mwo_token')
    
@frontend.route('/logout')
def logout():
    session['mwo_token'] = None
    get_current_user(True)
    flash('You were logged out!', 'success')
    return redirect(url_for('index'))
    
@frontend.route('/login')
def login():
    session['mwo_token'] = None
    session['username'] = None
    
    redirector = mwoauth.authorize()

    # Another workaround: MW's authorize requires an oauth_consumer_key, while e.g. twitter and facebook don't
    redirector.headers['Location'] += "&oauth_consumer_key=" + mwoauth.consumer_key
    return redirector

def get_current_user(cached=True):
    if cached:
        return session.get('username')
    
    try:
        # Another hack: we need to use the Authorized: header.
        # Using .get will append the OAuth stuff to the request string
        # Using .post without non-form content type will add it to the form data (default for .post)
        data = mwoauth.post("https://www.mediawiki.org/w/api.php?action=query&meta=userinfo&format=json", content_type="text/plain").data
        session['username'] = data['query']['userinfo']['name']
    except KeyError:
        session['username'] = None
        if data['error']['code'] == "mwoauth-invalid-authorization":
            flash(u'Access to this application was revoked. Please re-login!', 'success')
        else:
            raise
    except OAuthException:
        session['username'] = None
    return session['username']
    
@app.route('/oauth-callback')
@mwoauth.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next', url_for('.index'))
    if resp is None:
        flash(u'You denied the request to sign in.', 'danger')
        return redirect(next_url)

    session['mwo_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    
    get_current_user(False)
    
    flash('You are now logged in, %s!' % get_current_user(), 'success')
    return redirect(next_url)

##############################

@frontend.route('/')
@langswitch
def index():
    return render('index.html')

@frontend.route('/tools/')
@langswitch
def alltools():
    return render('alltools.html', tools=tools)

@frontend.route('/about/')
@langswitch
def about():
    return render('about.html')