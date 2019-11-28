import requests
from flask import Flask
from flask import jsonify

ip = ''

url = 'http://'+ip+':5000/'
app = Flask(__name__)

@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
	print(url+u_path)
	r = requests.get(url+u_path)
	resp = jsonify(r.json())
	return(resp)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)