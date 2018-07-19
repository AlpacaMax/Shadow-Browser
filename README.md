#Shadow-Browser

Bypass firewalls through an online browser

##Requirements
* docker
* docker-compose
##Server
1. Open 'docker-compose.yml'
2. Go to line '21' and change
'''
-HOSTNAME = 127.0.0.1
'''
into
'''
-HOSTNAME = Your server's ip address or domain
'''
3. 
'''
service docker start
docker-compose up
'''
###Usage
1. Open your browser and type in your server's ip address or domain

2. Follow the instruction and you will get a browser