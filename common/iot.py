import os
from urllib import request
import json
import time

class hass:
    def __init__(self):
        self.auth=None
        self.url=None

    def set_auth(self, auth):
        self.auth = auth
    
    def set_url(self, url):
        if url[:4] == "http":
            self.url=url
        else:
            if url.find(':') == -1:
                self.url="http://{}:8123/api/services".format(url)
            else:
                self.url="http://{}/api/services".format(url)

    def switch(self, id, on):
        if self.url == None or self.auth == None:
            print("please set the home assistant url and authenication token")
            return

        cmd = "turn_off"
        
        if on == True:
            cmd = "turn_on"

        url = "{}/switch/{}".format(self.url, cmd)
        req = request.Request(url, method="POST")
        req.add_header('Authorization','Bearer {}'.format(self.auth))

        data = {
            "entity_id": id
        }

        data = json.dumps(data)
        data = data.encode()
        r = request.urlopen(req, data=data)
        content = r.read()