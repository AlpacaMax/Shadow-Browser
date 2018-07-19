from flask import *
import requests
import os

app = Flask(__name__)

SECRET = os.environ.get("SECRET")
HOSTNAME = os.environ.get("HOSTNAME")


def validate_token(token, hashes, secret):
    api_url = "https://api.coinhive.com/token/verify"

    data = {
        'token': token,
        'hashes': hashes,
        'secret': secret
    }

    r = requests.post(api_url, data)

    return r.text.find('true') > 0


def get_page(url):
    return requests.get(url).text


@app.route("/")
def index():
    host = HOSTNAME
    info = get_page("http://docker_api/browsers_info")
    info_list = info.split("#")
    avail = info_list[0]
    inuse = info_list[1]
    per_avail = info_list[2]
    per_inuse = info_list[3]
    return render_template('index.html', hostname=host, 
                                         available=avail, 
                                         inuse=inuse,
                                         per_available=per_avail,
                                         per_inuse=per_inuse)


@app.route("/get_browser/<token>")
def get_browser(token):
    if validate_token(str(token), 256, SECRET):
        out = get_page("http://docker_api/run_chrome?duration=" + str(300))
        out_list = out.split("#")
        hostname = out_list[0]
        port = out_list[1]
        password = out_list[2]
        return render_template('launch.html', hostname=hostname, port=port, password=password)
    else:
        return "Invalid token! Please play fair!"


@app.route("/helloworld")
def hello():
    return get_page('http://docker_api/')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
