
import uuid
from dbhelpers import conn_exe_close
from apihelpers import get_display_results, verify_endpoints_info
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4

app = Flask(__name__)


@app.post('/api/client')
def login_client():
    invalid = verify_endpoints_info(request.json,['email','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str),400)
    token = uuid4().hex
    results = get_display_results('call login_client(?,?,?)',
    [request.json.get('email'),request.json.get('password'),token])
    # return make_response(json.dumps(results,default=str),200)
    if(results[0][0] == 1):
        return make_response(json.dumps(token,default=str),200)
    elif(results[0][0] == 0):
        return make_response(json.dumps('Invalid Credentials for Login',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)
    

if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    import bjoern #type: ignore
    bjoern.run(app,'0.0.0.0',5002)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


