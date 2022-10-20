
from dbhelpers import conn_exe_close
from apihelpers import get_display_results, verify_endpoints_info
from flask import Flask, request, make_response
import json
import dbcreds
import secrets

app = Flask(__name__)

def check_client():
    invalid = verify_endpoints_info(request.json,['email','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call ask_credentials(?,?)',
    [request.json.get('email'),request.json.get('password')])
    return results

def insert_token(client_id):
    token = secrets.token_hex(20)
    results = get_display_results('call add_id_token(?,?)',[client_id,token])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json

@app.post('/api/client')
def login_client():
    client_id = check_client()
    if(type(client_id) == list):
        token = insert_token(client_id[0][0])
        return token

if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    import bjoern #type: ignore
    bjoern.run(app,'0.0.0.0',5002)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


