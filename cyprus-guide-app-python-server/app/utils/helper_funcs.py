from app import session, redirect, url_for, abort, firestore
import json, jwt, datetime
import hashlib
import secrets
import requests
import base64


# redis_client = redis 
NODE_SERVER_URL = 'http://localhost:5030'
# NODE_SERVER_URL = 'https://pickr-geo-server-v1.herokuapp.com'

def logout():
    try:
        session.pop('email', None)
        session.pop('idToken', None)
        return redirect(url_for('index'))
    except:
        return abort(401, description="ERROR LOGGING USER OUT")



def encrypt_password(password):

    salt = b'YTkO/4R2MufJX9n6sSONjg=='
    # salt = secrets.token_bytes(16)
    salted_password = salt + b'$' + bytes(password, "utf-8")
    hashed = hashlib.md5(salted_password)
    result = {
        "algorithm": "MD5",
        "salt": base64.b64encode(salt).decode("ascii"),
        "saltOrder": "PREFIX",
        "value": base64.b64encode(hashed.digest()).decode("ascii"),
    }
    return result


def get_user_id_from_cache():
    
    user = load_cached(session["email"])
    return user["idToken"]

def hash_cordinates( data ):
    try:
        pos = requests.post(f'{NODE_SERVER_URL}/get_hash', params=f'data={json.dumps({"name" : data[u"area_name"],"position": { "lon": data[u"longitude"], "lat":data[u"latitude"] }})}')
        
        if pos.status_code == 200:
            pos.close()
            _pos = pos.json()
            _pos = _pos["position"]
            pos_data = {
                "geohash": _pos["geohash"],
                "geopoint": firestore.GeoPoint(_pos["geopoint"]["_latitude"], _pos["geopoint"]["_longitude"])
            }
        
            return pos_data
        else:
            pos.close()
            return pos.status_code
    except ConnectionError as err:
        
        return {
            "status": "failed",
            "message": "Connection to map function server failed",
            "exceptionThrown": err,
            "code": 500
        }

        

def get_node_nearby_places( data ):
    try:
        places = requests.get(f'{NODE_SERVER_URL}/nearby_places', params=f'data={json.dumps({"country" : data[u"country"], "places": data[u"places"], "region": data[u"region"], "longitude":data[u"longitude"], "latitude":data[u"latitude"], "radius": data[u"radius"] })}')
    
        if places.status_code == 200:
            return places.json()
        else:
            return places.status_code
    except ConnectionAbortedError as err:
        return {
            "status": "failed",
            "message": "Connection to map function server Was Aborted",
            "exceptionThrown": err,
            "code": 500
        }

    except ConnectionError as err:
       return {
            "status": "failed",
            "message": "Connection to map function server failed",
            "exceptionThrown": err,
            "code": 500
        }

    finally:
        places.close()



def get_guide_nearby_places( data ):
    try:
        places = requests.post(f'{NODE_SERVER_URL}/nearby_places', json=data)
    
        if places.status_code == 200:
            return places.json()
        else:
            return {
                "status": "failed",
                "message": "Connection to map function server Was Aborted",
                "exceptionThrown": places.content,
                "code": places.status_code
            }
    except ConnectionAbortedError as err:
        return {
            "status": "failed",
            "message": "Connection to map function server Was Aborted",
            "exceptionThrown": err,
            "code": 500
        }

    except ConnectionError as err:
       return {
            "status": "failed",
            "message": "Connection to map function server failed",
            "exceptionThrown": err,
            "code": 500
        }

    finally:
        places.close()


def get_guide_filtered_places( data ):
    try:
        places = requests.post(f'{NODE_SERVER_URL}/nearby_filtered_places', json=data)
    
        if places.status_code == 200:
            return places.json()
        else:
            return places.status_code
    except ConnectionAbortedError as err:
        return {
            "status": "failed",
            "message": "Connection to map function server Was Aborted",
            "exceptionThrown": err,
            "code": 500
        }

    except ConnectionError as err:
       return {
            "status": "failed",
            "message": "Connection to map function server failed",
            "exceptionThrown": err,
            "code": 500
        }

    finally:
        places.close()



def do_return( data ):
    if data["code"] == 200:
        return data, 200
            
    elif data["code"] == 400:
        return data, 400
    
    else:
        return data, 200




def only_changed( data ):
    contraband = [[],{},""]
    count = 0

    for key in list(data):
        if data[key] in contraband:
            del data[key]
            count += 1

    if "created_at" in data and count > 0:
        del data["created_at"]

    return data

def calc_rating( rating ):
    sum = rating["1"] + rating["2"] + rating["3"] + rating["4"] + rating["5"]
    return ((1*rating["1"]) + (2 * rating["2"]) + (3 * rating["3"]) + (4 * rating["4"]) + (5 * rating["5"]) / sum)

def get_login_token (data, user, private_key):
    try:
        return jwt.encode({
            "user": {"display_name": data['display_name'], "photo_url": data['photo_url']},
            "iss": "pickr-admin.io",
            "sub": user,
            # "aud": ["pickr.web", "pickr.mobile"],
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(seconds=120)
        },str(private_key[0]), algorithm="RS256")

    except Exception as err:
        return {
            "status": "failed",
            "message": "Failed to encode Data",
            "exceptionThrown": err,
            "code": 'ENCODNG_ERROR'
        }

def get_refresh_token (data, user, private_key):
    try:
        return jwt.encode({
            "user": {"display_name": data['display_name'], "photo_url": data['photo_url']},
            "iss": "pickr-admin.io",
            "sub": user,
            # "aud": ["pickr.web", "pickr.mobile"],
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(days=7)
        },str(private_key[0]), algorithm="RS256")

    except Exception as err:
        return {
            "status": "failed",
            "message": "Failed to encode Data",
            "exceptionThrown": err,
            "code": 'ENCODNG_ERROR'
        }

def new_user_session( data, user, private_key):
    token = get_login_token( data, user, private_key)
    refresh_token = get_refresh_token( data, user, private_key)
    return {
        "token": token,
        "refresh_token": refresh_token
    }

def decode_token ( encoded, public_key ):
    try:
        decoded = jwt.decode(encoded, str(public_key[0]), algorithms="RS256")
        return decoded
    except jwt.ExpiredSignatureError as err:
        return {
            "status": "failed",
            "message": "Token Signature Expired",
            "exceptionThrown": err,
            "code": 'EXPIRED_SIGNATURE'
        }
    except jwt.InvalidTokenError as err:
        return {
            "status": "failed",
            "message": "Token is Invalid",
            "exceptionThrown": err,
            "code": 'INVALID_TOKEN'
        }
    except jwt.InvalidAudienceError as err:
        return {
            "status": "failed",
            "message": "Token Audience is invalid",
            "exceptionThrown": err,
            "code": 'INVALID_TOKEN_AUDIENCE'
        }
    except jwt.ImmatureSignatureError as err:
        return {
            "status": "failed",
            "message": "Token Signature is Immature",
            "exceptionThrown": err,
            "code": 'IMMATURE_TOKEN_SIGNATURE'
        }
    except jwt.InvalidIssuerError as err:
        return {
            "status": "failed",
            "message": "Token Issuer Is Invalid",
            "exceptionThrown": err,
            "code": 'INVALID_ISSUER_ERROR'
        }
    except jwt.InvalidKeyError as err:
       return {
            "status": "failed",
            "message": "Token Key Error",
            "exceptionThrown": err,
            "code": 'TOKEN_KEY_ERROR'
        }
    except jwt.PyJWTError as err:
        return {
            "status": "failed",
            "message": "Token Validation Failed",
            "exceptionThrown": err,
            "code": 'UNKOWN_ERROR'
        }

