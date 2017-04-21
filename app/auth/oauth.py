import json
import requests
from rauth import OAuth1Service, OAuth2Service
from flask import url_for
from flask import (
    current_app,
    session,
    request,
    redirect
)
# ==================================


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]
# ==================================


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )
    # __________________________________

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )

        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))
    # ______________________________

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None   # Twitter does not provide email
    # ______________________________
# ==================================


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        google_params = requests.get('https://accounts.google.com/.well-known/openid-configuration').json()
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google_params.get('authorization_endpoint'),
            base_url=google_params.get('userinfo_endpoint'),
            access_token_url=google_params.get('token_endpoint')
        )
    # _____________________________________

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                scope='email',
                response_type='code',
                redirect_uri=self.get_callback_url()
            )
        )
    # ______________________________________

    def callback(self):
        if 'code' not in request.args:
            return None, None, None

        code = request.args['code'],
        print("Code: {}".format(code))
        print("Code type: {}".format(type(code)))
        redirect_uri = self.get_callback_url()
        print("Redirect URI: {}".format(redirect_uri))
        print("Redirect URI type: {}".format(type(redirect_uri)))

        oauth_session = self.service.get_auth_session(
            data={
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },

            decoder=lambda b: json.loads(b.decode('utf-8'))
        )

        me = oauth_session.get('').json()
        print("Google ME: {}".format(me))
        social_id = 'google$' + str(me.get('sub'))
        return social_id, me['email'], me['email']
