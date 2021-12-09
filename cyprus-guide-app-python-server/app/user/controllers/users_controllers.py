from hashlib import new
from app import auth, db, session, abort, firestore, jwt, os, config, make_response
from app.user.models.user_model import User, Tags
# from flask_login import login_user, login_required, logout_user, current_user 
from app.utils.helper_funcs import decode_token, get_login_token, get_user_id_from_cache, new_user_session
import pem

dirname = os.path.dirname(__file__)



private_key = pem.parse_file(os.path.join(dirname, '../../../privatekey.pem'))
public_key = pem.parse_file(os.path.join(dirname, '../../../publickey.pem'))
assert isinstance(public_key, list )
assert isinstance(private_key, list )

# print(public_key[0])

# assert isinstance(private_key, pem.ser )

def register_new_user(data):

    # init variables
    email = data[u'email']
    password = data[u'password']
    # phone_number = data[u'phone_number']
    display_name = data[u'display_name']
    photo_url = ""

    # using dummy photourl if none is provided
    if u'photo_url' in data:
        photo_url = data[u'photo_url']
    else:
        photo_url = u'https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg'

    # create user if email and password are present
    if(email != None and password != None):
        try:
            user = auth.create_user(
                    email=email,
                    email_verified=False,
                    # phone_number=u'+' + phone_number,
                    password=password,
                    display_name=display_name,
                    photo_url=  photo_url,
                    disabled=False
                )
        except Exception as err:
            abort(409, description=f"{err}")
            return {
                "error": err
            }

        # set session and create jwt token if user is created 
        if(user):
            user_object = User(email=email,display_name=display_name, photo_url=photo_url, email_verified=False, disabled=False, phone_number="")
            db.collection(u'users').document(user.uid).set(user_object.to_dict())
            session['email'] = email
            session['idToken'] = user.uid

            # return user_object.to_dict()

            encoded = new_user_session(user_object.to_dict(), user.uid, private_key )

            if 'code' in encoded and 'exceptionThrown' in encoded:
                return {
                    abort(401, description=encoded)
                }
            else:
                set_user_token( encoded['refresh_token'])
                return encoded

        return abort(401, description="EMAIL AND PASSWORD ARE REQUIRED")





def sign_user_in(data):

    # init variables
    email = data['email']

    # fetch user if email elsse abort
    if(email != None ):
        user = auth.get_user_by_email(email)

        # if user exists, get user datat from fb and send data in JWT token to requester
        if(user):
            session['email'] = email
            session['idToken'] = user.uid
        
        user_data = db.collection('users').document(user.uid).get()

        # encode user data and form token
        encoded = new_user_session(user_data.to_dict(), user.uid, private_key )


        # return token is no errors occur
        if encoded and encoded != "":
            if 'code' in encoded and 'exceptionThrown' in encoded:
                return {
                    abort(401, description=encoded)
                }
            else:
                set_user_token( encoded['refresh_token'] )
                return encoded

    else:
        return abort(401, description="EMAIL IS REQUIRED")




def signout_user( token ):
    try:
        if 'email' in session and 'idToken' in session:
            unset_user_token(token)
            session.pop('email', None)
            session.pop('idToken', None)
            return { 'status': 'logged_out' }
    except:
        return abort(401, description="ERROR LOGGING OUT...TRY AGAIN")




def get_user_data(uid):
    doc_ref = db.collection('users').document(uid)

    doc = doc_ref.get()
    # print(doc.to_dict())
    user = User.from_dict(doc.to_dict())
    return user.to_dict()



def update_user_tags(data):
    try:
        doc_ref = db.collection('users').document(get_user_id_from_cache())
        # doc = doc_ref.set({}, merge=True)
        doc = doc_ref.update(
            {u'tags': firestore.ArrayUnion(Tags(data).to_list())})
        tags = Tags.from_list(doc_ref.get().to_dict()[u'tags'])
        return tags
    except:
        return "Failed To Update User Tags", 401



def set_user_token( token ):
    try:
        doc_ref = db.collection('users').document(session['idToken'])
        doc_ref.update({
            'rToken': token
        })
    except Exception as err:
        return f'Failed To set user Token: {err}'


def unset_user_token( token ):
    try:
        parse_token = decode_token(token, public_key)
        doc_ref = db.collection('users').document(parse_token['sub'])
        doc_ref.update({
            'rToken': ''
        })
    except Exception as err:
        return f'Failed To set user Token: {err}'


def user_token_is_valid( token ):
    try:
        doc_ref = db.collection('users').document(session['idToken'])
        user = doc_ref.get().to_dict()
        if 'rToken' in user and user['rToken'] == token:
            return token
        else:
            return False
        
    except Exception as err:
        return f'Failed To set user Token: {err}'



def refresh_user_token( token, uid):
    print(f'Token: {token}  \n Uid: {uid}')
    try:
        extended_session = extend_user_token(token, uid, public_key, private_key)

        if 'token' in extended_session:
            return extended_session
        else:
            encoded = new_user_session(extended_session['user'], uid, private_key)
            set_user_token( encoded['refresh_token'] )
            return encoded
    except Exception as err:
        return {
            "status": "Refresh Token Failed",
            "message": err,
            "exceptionThrown": "INVALID_TOKEN",
            "code": 'INVALID_TOKEN'
        }



def check_token( etoken ):
    try:
        token = decode_token(etoken, public_key)
    except Exception as err:
        return f"Token could not be Verified {err}"
    else:
        if user_token_is_valid( etoken ):
            return True
        else:
            response = make_response({ "user": None })
            response.set_cookie('refresh_token', value=b'', expires=0)
            signout_user()
            token =  {
            "status": "Logged Out",
            "message": "Token is Invalid",
            "exceptionThrown": "INVALID_TOKEN",
            "code": 'INVALID_TOKEN'
        }
    finally:
        return token





def extend_user_token( encoded_rToken, user, public_key, private_key):
    token = ""
    new_session = {}
    try:
        token = decode_token(encoded_rToken, public_key )
    except Exception as err:
        return f'Token Validation Error: {err}'

    else:
        if user_token_is_valid( encoded_rToken ):
            new_session = new_user_session( token['user'], user, private_key )
        else:
            new_session = check_token(encoded_rToken)
    finally:
        return new_session



def update_user_data(data):
    try:
        if u'email' in data:
            del data[u'email']

        if u'phone_number' in data:
            del data[u'phone_number']

        if u'photo_url' in data:
            del data[u'photo_url']

        if u'password' in data:
            del data[u'password']

        doc_ref = db.collection('users').document(get_user_id_from_cache())
        print(f' =============> {data} ')
        doc = doc_ref.set(data, merge=True)
        data = User.from_dict(doc_ref.get().to_dict())
        return data.to_dict()
    except:
        return "Failed To Update User Tags", 401
