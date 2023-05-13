import base64
import sys
import pydicom
import json

from flask import Flask, render_template, request, jsonify, Response, make_response

app = Flask(__name__, static_folder='templates', static_url_path='', template_folder='templates')
data = []


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')



@app.route('/data')
def get_data():
    global data
    return json.dumps(data)



def process_files(files):
    for i in range(len(files)):
        DC = pydicom.dcmread(files[i], force=True)

        DC_J = DC.to_json_dict()

        if ('00420011' in DC):
            print(len(DC['00420011'].value))
            DC_J['00420011']['InlineBinary'] = base64.b64encode(DC['00420011'].value).decode('utf-8')
            print(len(DC_J['00420011']['InlineBinary']))
            data.append(DC_J)

if __name__ == '__main__':
    sub = []
    for i in range(1,len(sys.argv)):
        sub.append(sys.argv[i])
    process_files(sub)

    app.run(debug=True,threaded=True,use_reloader=False)
