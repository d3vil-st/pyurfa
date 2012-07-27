# -*- coding: utf-8 -*-

import struct

class URFAClient_Packet:
    
    version = 35
    code = 0
    len = 4
    iterator = 0
    sock = False
    data = []
    
    def __init__(self, socket):
        self.sock = socket.socket
        self.clean()
    
    def clean(self):
        self.code = 0
        self.len = 4
        self.iterator = 0
        self.attr = {}
        self.data = []
        
    def read(self):
        self.code = int(ord(self.sock.recv(1)))
        version = int(ord(self.sock.recv(1)))
        if self.version != version:
            print "Version error"
            return
        
        self.len = int(struct.unpack(">h",self.sock.recv(2))[0])
        self.parse_data()

    def write(self):
        self.sock.send(chr(self.code))
        self.sock.send(chr(self.version))
        self.sock.send(struct.pack(">H",self.len))
        for code in self.attr:
            self.sock.send(struct.pack("<H", code))
            self.sock.send(struct.pack(">H", self.attr[code]['len']))
            self.sock.send(self.attr[code]['data'])
            
        for data in self.data:
            self.sock.send(struct.pack("<H", 5))
            self.sock.send(struct.pack(">H", len(data)+4))
            if len(data)>0:
                self.sock.send(str(data))

    def parse_data(self):
        tmp_len = 4
        
        while tmp_len < self.len:
            code = int(struct.unpack("h",self.sock.recv(2))[0])
            length = int(struct.unpack(">H",self.sock.recv(2))[0])
            tmp_len += length
            
            if length == 4:
                data = None
            
            else:
                data = self.sock.recv(length - 4)
                
            if code == 5:
                self.data.append(data)
            
            else:
                self.attr = { code: ({ 'data': data, 'len': length }) }
            
    def AttrSetString(self, string, code):
        self.attr.update({code:({'data': string, 'len': (len(string)+4)})})
        self.len += len(string) + 4
        #print "AttrSetString:", self.len
        
    def AttrSetInt(self, attr, code):
        attr = struct.pack(">L", attr)
        self.attr.update({code:({'data': attr, 'len': 8})})
        self.len += 8
        #print "AttrSetInt:", self.len
        
    def AttrGetInt(self, code):
        if self.attr[code]['data']:
            return int(struct.unpack(">L", self.attr[code]['data'])[0])
        else:
            return False
    
    def DataSetInt(self,data):
        data = struct.pack(">L", data)
        self.data.append(data)
        self.len += 8
        
    def DataGetString(self):
        num = self.iterator
        self.iterator += 1
        return str(self.data[num])
    
    def DataGetInt(self):
        num = self.iterator
        self.iterator += 1
        return int(struct.unpack(">L2",self.data[num])[0])
    
    def DataGetDouble(self):
        num = self.iterator
        self.iterator += 1
        return float(struct.unpack("d",str(self.data[num])[::-1])[0])
