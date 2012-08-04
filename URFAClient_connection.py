
# -*- coding: utf-8 -*-

import socket, hashlib, ssl

from URFAClient_Packet import URFAClient_Packet

class URFAClient_connection():
    error = False
    error_message = ""
    __socket = None
    
    def __init__(self, address, port, login, password, ssl = None):
        if address and port and login:
            self.open(address, port)
            if (not self.error):
                self.login(login, password)

    def open(self, address, port):
        self.socket = socket.socket(
                          socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((address,port))
        except socket.error as message:
            self.error = True
            self.error_message = message
        
        #print self.socket.recv(64)


    def __del__(self):
        self.socket.shutdown(1)

    def login(self, login, password):
        packet = self.getPacket()
        packet.read()
        if packet.code == 192:
            self.urfa_auth(packet, login, password)
        
        packet.read()
        if packet.code == 194:
            if packet.AttrGetInt(10):
                ssl.wrap_socket(self.socket)


    def close(self):
        self.__del__()

    def __call__(self):
        return self.socket

    def getPacket(self):
        return URFAClient_Packet(self)

    def urfa_auth(self, packet, login, password):
        ssl = 0
        digest = packet.attr[6]['data']
        ctx = hashlib.md5()
        ctx.update(digest)
        ctx.update(password)
        passhash = ctx.digest()
        packet.clean()
        packet.code = 193
        packet.AttrSetString(login, 2)
        packet.AttrSetString(digest, 8)
        packet.AttrSetString(passhash, 9)
        packet.AttrSetInt(ssl,10)
        packet.AttrSetInt(2,1)
        packet.write()
        
    def urfa_call(self, code):
        packet = self.getPacket()
        packet.clean()
        packet.code = 201
        packet.AttrSetInt(code, 3)
        packet.write()
        packet.clean()
        
        packet.read()
        if packet.code == 200:
            if packet.AttrGetInt(3) == code:
                return True
            else:
                return False
        else:
            return False
        
    def urfa_get_data(self, data = False):
        packet = self.getPacket()
        packet.read()
        if packet.code == 200:
            try:
                packet.AttrGetInt(4)
            except KeyError:
                return packet
            else:
                return None
    
    def urfa_send_param(self, packet):
        packet.code = 200
        packet.write()
