# -*- coding: utf-8 -*-

from URFAClient import URFAClient

bill = URFAClient("hostname", 11758, "login", "password")

acoount_info = bill.rpcf_get_accountinfo(523)
print acoount_info['balance']

bill.close()