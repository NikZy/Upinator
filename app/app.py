from flask import Flask
from flask import request
from flask import jsonify
import os
from pushbullet import Pushbullet
app = Flask(__name__)
class Ip:
    def __init__(self):
        self.ip = ""
        self.pb = Pushbullet(os.environ.get("PUSHBULLET"))

@app.route('/')
def hello_world():
    return 'Hello, World!2'

ip = Ip()
@app.route("/ip", methods=["GET"])


def get_my_ip():

    if (ip.ip != request.environ.get('HTTP_X_REAL_IP', request.remote_addr)):
        #ip.ip = request.remote_addr
        ip.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        ip.pb.push_note("IP Changed!", ip.ip)
        return jsonify({'homo': "test"}), 200
    
#    return jsonify({'ip': request.remote_addr}), 200
    return jsonify({'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)})

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')

