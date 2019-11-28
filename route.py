import requests
from flask import Flask 

url = '18.204.216.201:5000/'
app = Flask(__name__)

@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))
    r = requests.get(url)
	print(r.json())
    print('You want path: %s' % u_path)
    return(r.json())

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)