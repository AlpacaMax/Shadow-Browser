from flask import Flask
import docker
from flask import request
from threading import Timer
import random
import os

app = Flask(__name__)

MIN_PORT = 5950  # Min port for vnc services
MAX_PORT = 6000  # Max port for vnc services (Not included)
TOTAL = MAX_PORT - MIN_PORT

ports_in_use = []

client = docker.from_env()

HOSTNAME = os.environ.get("HOSTNAME")
print("HOSTNAME:", HOSTNAME)


@app.route("/")
def hello():
    """
    Hello-world test
    """
    txt = client.containers.run('alpine', 'echo hello world, alpine')
    return txt.decode('ascii')


def get_port():
    """
    get an available port no in use
    return -1 if no port available
    """
    for port in range(MIN_PORT, MAX_PORT):
        if not (port in ports_in_use):
            ports_in_use.append(port)
            return port
    return -1


def release_port(port):
    """
    release a port from the pool
    return 0 if successful
    return -1 if not successful
    """
    if port in ports_in_use:
        ports_in_use.remove(port)
    else:
        raise Exception('Port not in use!')


def kill_container(container, port):
    print(container.id + " killed!")
    container.kill()
    release_port(port)


def start_chrome_container(port, duration, password):
    """
    start a container on port with duration and password
    duration in second
    """
    container = client.containers.run('siomiz/chrome', ports={'5900/tcp': ('0.0.0.0', port)},
                                      detach=True, auto_remove=True,
                                      environment=['VNC_PASSWORD=' + str(password)])
    Timer(duration, kill_container, (container, port, )).start()


@app.route("/run_chrome", methods=['GET'])
def run_chrome():
    """
    example: http://localhost/run_chrome?duration=5
    duration: the duration of a container in minutes
    duration = -1 for unlimited time
    return: the port of the service
    """
    duration = request.args.get('duration')
    port = get_port()
    password = random.randint(0, 99999999)
    start_chrome_container(port, int(duration), password)
    out = HOSTNAME + "#" + str(port) + "#" + str(password)
    return out


@app.route("/hostname")
def hostname():
    """
    check if the hostname is correct
    :return: the host name of the server
    """
    return HOSTNAME

@app.route("/browsers_info")
def get_info():
    inuse = len(ports_in_use)
    available = TOTAL - inuse
    per_inuse = int(float(inuse) / TOTAL * 100)
    per_available = int(float(available) / TOTAL * 100)
    info = str(available) + "#" + str(inuse) + "#" + str(per_available) + "#" + str(per_inuse)
    return info

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
