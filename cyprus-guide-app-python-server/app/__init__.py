import os
from flask import Flask, request, session, url_for, redirect, jsonify, make_response
from flask.helpers import send_from_directory
from flask_cors import CORS
from decouple import config
import jwt
from flask_restful import Api, Resource, reqparse, abort

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore



app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

# Flask Secrect Key

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "ncapp-660ed",
  "private_key_id": "0b5cd99a5b4bb9eda4b3a6d23cc02bae57a86c1d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDDpkugQ+BJ+ZGt\n7XvuultKlIAg/bEooPhZxegNGY33hd4EqHYLzH8ZNFycctkCDYjSHCLV0qRHoXV3\nWLeDBHeMlLUVzU7aSKMdh0oGQ5qiOgppOsC1yQy1j9avH5gJvCAUla/ytzkfyBOY\ngLhTjQZXLBYZEDNGEQvjOSHuOQs38QZshxmdQKPzVavglz9oKyuIYHBknU2uMYRt\ne2h0a6Fj1mi1d4eN2fuxRFMZSi1SXhk3ASMHKSt/gGzVXczaISk/u59h3XWMF10g\nwccr2PdnRh2Zjid+qcmfhU67MHSvURmITjdabUsYg25d7SQWTp4zzDqQ2wDFRiGc\nZsbcVYevAgMBAAECgf89kGvJ5gOttS/Mw+3mMPbB8twlvlk5qInS0lcyq58Ama1f\nkPg+9xpct48XctNIJ2vmP9fSxiBA28ZwHOxMozelzAj2ffmK71BkiIMX50pr+rsT\nDGnQWDpurn778YNXxb5SgwCFQyJhMyJMvjRewMivwfbAXgNSlycKA7dwsIKB3nNJ\n/bSjqlO08FmilwW1MN2P8LYzh594Hc+pcd/EH/L65TpmhrK/iE4jrNXsmiN8QIrM\nG/Zw9Wglj7rHgnnPCZ8ycvzZTZ9mJo/LpBEWKxtTz55pVyr9aLgvKPj88Wr34YBn\ndFxL2Oy0jXvtdbmUF3pCr8lR0uwPSMIwWbWMfMkCgYEA9OpILKPrEHtB1+fKDX9H\nH9g/iBXMEYe65mg/755ORCkaNRUo+zTJoJsaNrbqm5ruc/EdJv9v/AcvNa892xO5\nAHs/ByBvBJu7vuwcCrFj3fkd8EWiKeTy/SvMzIlJoOJk1Tgyk1QFZBN74td+0FAh\nixq6LqAHqSrYmFSx3q0U8ZUCgYEAzIEyOyAOWzPKM5q2oDDz4QpvIcRW6eFgij6u\nSvgEI7GEzxxSHl36//g2jIgtOpM8thCe1TR27oRscb2NTUa3psk0U92jUhsZAZlY\nI2Qrvt9pUbJUbvS/IzISwf00R4wP2Xnp5RTtu5jgGhCsKlbTNUn7pu7i0RZq75bP\nAe2oCzMCgYAa8bNjBd2UgJrrz9pQxdHjVP0YUZ2TyCTtuEZgbEAcC5GQiXVqvZH5\nE1c88b65w7+8DaixY6TES14MP+1ELtVJkkWK2SydiyyKgptLKdzczM1YY7DFfySk\naa8sSWZKRt3k/zvBLZsyOVqFyENxU399OEGHY5+0IryVdavj3ZLSSQKBgQCloVHk\njx7xgO2YhAq7jUpIjqHZcGKQRChjb0bMkzkPC5yr/Z0I2UcL/6V2hmhTU6LNNoLd\n3QMiRQBr0oDaAJeHrtgBwLWhLy8+m0rGR0Ai9GEheNRnlTQlNk347bFk7Sx9D/9+\nuUeeM7/1fGFkXTPsqgH2fu4XOBfd+n+oaSo7/wKBgQCxDDVzcyXN6vszhhWuJsjJ\nFQaxPAg58P92mcZB2HrqbZjjY9qZLmVLfnJmXXbQMQRnesbyAhTai4T2BHmcIbAP\njQ9c39KEa9NJXYRmFcTvib2p98qhDwFPffF9NJC3cj+UwDK3Ksl4ZvvjHzQ5pARg\nj/3gQzUj/C5VjGiKVUrXuw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2qckf@ncapp-660ed.iam.gserviceaccount.com",
  "client_id": "115206092053927301679",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2qckf%40ncapp-660ed.iam.gserviceaccount.com"
}
)

firebase_admin.initialize_app(cred)
db = firestore.client()

from app.user.routes import user_routes
from app.places.routes import places_routes
from app.houses.routes import houses_routes
from app.tours.routes import routes