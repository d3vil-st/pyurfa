# -*- coding: utf-8 -*-
#import time

from URFAClient_connection import URFAClient_connection

class URFAClient_Admin(URFAClient_connection):
    def rpcf_get_accountinfo(self, account_id):
        data = {}
        if not self.urfa_call(0x2030):
            print "error calling function"
            return False
        #tmp = self.urfa_get_data()
        packet = self.getPacket()
        packet.DataSetInt(account_id)
        self.urfa_send_param(packet)
        tmp = self.urfa_get_data()
        data['unused'] = tmp.DataGetInt()
        data['is_blocked'] = tmp.DataGetInt()
        data['dealer_account_id'] = tmp.DataGetInt()
        data['is_dealer'] = tmp.DataGetInt()
        data['vat_rate'] = tmp.DataGetDouble()
        data['sale_tax_rate'] = tmp.DataGetDouble()
        data['comission_coefficient'] = tmp.DataGetDouble()
        data['default_comission_value'] = tmp.DataGetDouble()
        data['credit'] = tmp.DataGetDouble()
        data['balance'] = tmp.DataGetDouble()
        data['int_status'] = tmp.DataGetInt()
        data['block_recalc_abon'] = tmp.DataGetInt()
        data['block_recalc_prepaid'] = tmp.DataGetInt()
        data['unlimited'] = tmp.DataGetInt()
        self.urfa_get_data()
        return data
    
    def rpcf_core_build(self):
        data = {}
        if not self.urfa_call(0x0046):
            print "error calling function"
            return False
        tmp = self.urfa_get_data()
        data['core_build'] = tmp.DataGetString()
        self.urfa_get_data()
        return data