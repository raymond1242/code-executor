from flask import Flask, request, jsonify
from io import StringIO
from contextlib import redirect_stdout

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Docker!\n'


@app.route('/run', methods=['POST'])
def get_field():
    values = request.get_json()
    required = ['code']

    if not all(k in values for k in required):
        return 'Missing value CODE', 400
    code = values['code']
    try:
        f = StringIO()
        with redirect_stdout(f):
            exec(code)
        s = f.getvalue()
        response = {'response': 'success', 'body': f'{s}'}
    except Exception as e:
        response = {'response': 'error', 'body': f'{str(e)}'}

    return jsonify(response), 200
