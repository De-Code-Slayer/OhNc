from flask.helpers import make_response, send_from_directory
from app import app, auth, session, request, url_for, redirect, Resource, api, reqparse,os
import json
from app.user.controllers.authentication import logged_in
from app.user.controllers.users_controllers import refresh_user_token, register_new_user, sign_user_in, signout_user, get_user_data, update_user_data
import sys

# redis_client = redis
# q = Queue(connection=redis_client)
app.secret_key = b'_PrivateSessionKey1_1@@~~_'

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.ico')


class index(Resource):
    def __init__(self):
        self.session_authenticated = 'idToken' in session
    
    @logged_in
    def get(self):

        if self.session_authenticated:
            return f'Logged in as {session["idToken"]}', 201
        else:
            return "Not Logged In", 401



class email_sign_in(Resource):
    def __init__(self):

        # [** PARSE INCOMING DATA **]
        self.args = request.json

    def post(self):
        user = sign_user_in(self.args)
        response = make_response({ 'access_token' : user['token'] })
        response.set_cookie('refresh_token', value=user["refresh_token"], httponly=True, samesite="None", secure=True)
        return response

    @logged_in
    def get(self):
        return "Not logged in"

class refresh_token( Resource ):
    def __init__(self):
        self.args = request.json
        
    @logged_in
    def post(self):
        data = self.args
        print(f'REFRSH DATA: {data}')
        user = refresh_user_token(request.cookies.get('refresh_token'), data["uid"])
        if 'token' in user:
            response = make_response({ 'access_token' : user['token'] })
            response.set_cookie('refresh_token', value=user["refresh_token"], httponly=True, samesite="None", secure=True)
            print(f'TOKEN_RES: {response}')
            return response
        else:
            return f'{user}'

class email_signup(Resource):
    def __init__(self):

        # [** PARSE INCOMING DATA **]
        self.args = request.json

    def post(self):
        user = register_new_user( self.args )
        print(f'USER: {user}')
        return user
        response = make_response({ 'access_token' : user['token'] })
        response.set_cookie('refresh_token', value=user["refresh_token"], httponly=True)



class signout(Resource):

    def post(self):
        # [** SIGN UP USER **]
        
        user = signout_user(request.cookies.get('refresh_token'))
        response = make_response({'user': user})
        response.set_cookie('refresh_token',value = b'', expires=0)
        return response


class user(Resource):
    def __init__(self):
        self.args = request
    @logged_in
    def get(self):
        user = get_user_data(self.args.json['uid'])
        response = make_response({ 'user' : user })
        return response


class update_user_account(Resource):

    def __init__(self):
        self.session_authenticated = 'idToken' in session
        self.args = request.json

    def post(self):
        if self.session_authenticated:
            user = update_user_data(self.args)
            if user:
                return user, 201
            else:
                return user
    pass


class delete_user_account(Resource):
    pass



class remove_attributes(Resource):
    # accept single key or list of keys
    pass


# api.add_resource(home, '/home', endpoint="home")
api.add_resource(index, '/api', endpoint="index")
api.add_resource(email_sign_in, '/api/auth/email_sign_in', endpoint="email_sign_in")
api.add_resource(email_signup, '/api/auth/email_signup', endpoint="email_signup")
api.add_resource(signout, '/api/user/signout', endpoint="signout")
api.add_resource(user, '/api/user', endpoint="user")
api.add_resource(update_user_account, '/api/user/update', endpoint="update_user_account")
api.add_resource(delete_user_account, '/api/user/delete', endpoint="delete_user_account")

# api.add_resource(add_places, '/api/user/add_places', endpoint="add_places")
api.add_resource(remove_attributes, '/api/user/remove_attribute', endpoint="remove_attribute")
# api.add_resource(add_news, '/api/user/add_news', endpoint="add_news")
api.add_resource(refresh_token, '/api/auth/refresh_token', endpoint="refresh_token")
