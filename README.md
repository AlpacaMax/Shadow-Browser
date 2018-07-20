# Shadow-Browser
A creative method to pass firewalls

## Introduction
Conventionally we use VPN or proxy server to bypass firewalls and log in websites we couldn't log in. The idea of shadow_browser is to create a browser on the server and users can connect to the browser with a webpage version of VNC called [noVNC](http://novnc.com) and use the online browser to surf the Internet.

## Server

### Requirement
* docker-cm
* docker-compose

### Configuration
1. Open `docker-compose.yml`
2. Goto ***Line 21***
3. Change
```
  -HOSTNAME = 127.0.0.1
```
into
```
  -HOSTNAME = your server's ip address or domain
```
4. Do the same thing for `env.env`
5. Make sure your server's ports from `5950` to `6000` and port `80` are not occupied
6. Open a terminal and type
```
shadow_browser # service docker start
shadow_browser # docker-compose up
```

## Usage
1. Open your browser on your computer
2. Enter you server's ip address or domain
3. Follow the instructions on the webpage
4. Enjoy yourself

### Demo
[shadow-browser](103.115.49.177)
