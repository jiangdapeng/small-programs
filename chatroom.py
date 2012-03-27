#!/usr/bin/env python

"""
@file chatroom.py
@brief a small chat room server
@author asuwill.jdp@gmail.com
@note what can be used as a chat client?
    telnet can be used in this way(both windows and xnix):
    telnet ip port 
    in which, ip is the machine's ip where chat server is running
    port is the port server listening
"""

import sys
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class ChatRoom(LineReceiver):
    
    def __init__(self,users):
        """docstring for __"""
        self.users = users
        self.name = None
        self.state= "LOGIN"
    def connectionMade(self):
        """docstring for connectionMade"""
        self.sendLine("Welcome to Chartroom\nWhat's your name?")
    
    def connectionLost(self,reason):
        """docstring for connectionLost"""
        if self.users.has_key(self.name):
            del self.users[self.name]
        line = "%s leaving char room" % (self.name,)
        for name,user in self.users.iteritems():
                user.sendLine(line)

    def lineReceived(self,data):
        """docstring for dataReceived"""
        data = data.strip()
        if self.state == "LOGIN":
            self.handle_LOGIN(data)
        else:
            self.handle_CHAT(data)
    def handle_LOGIN(self,data):
        """docstring for handle_LOGIN"""
        if self.users.has_key(data):
            self.sendLine("%s has been used. Please choose another name" % (data,))
        else:
            self.state = "CHAT"
            self.name = data
            self.users[data]=self
            self.sendLine("Welcome, %s" % (data,))
            line="%s come in" % (self.name)
            for name,user in self.users.iteritems():
                if user != self:
                    user.sendLine(line)
    def handle_CHAT(self,data):
        """docstring for handle_CHAT"""
        line="<%s>says:%s" % (self.name,data)
        for name,user in self.users.iteritems():
            if user != self:
                user.sendLine(line)
class ChatFactory(Factory):

    def __init__(self):
        """docstring for __init__"""
        self.users={}

    def buildProtocol(self,addr):
        """docstring for buildProtocol"""
        return ChatRoom(self.users)

def usage():
    """docstring for usage"""
    print("""usage:python chatroom.py port""")
    exit()

def main(argv):
    port=int(argv[0])
    reactor.listenTCP(port,ChatFactory())
    reactor.run()

if __name__=='__main__':
    if len(sys.argv)!=2:
        usage()
    else:
        main(sys.argv[1:])
