import re
import json
import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # prefix, label = message['path'].decode('ascii').strip('/').split('/') 
    label = "chris"
    Group('youPotify-' + label).add(message.reply_channel)
    message.channel_session['label'] = label
    
@channel_session
def ws_receive(message):
    print ">>> received message"
    data = json.loads(message['text'])
    # print data['sender']
    # print data['message']
    # label = message.channel_session['label']
    # print label
    label = "chris"
    Group('youPotify-' + label).send({'text' : json.dumps(data)})
    

@channel_session
def ws_disconnect(message):
    pass
