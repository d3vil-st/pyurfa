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
    
    def rpcf_change_intstat_for_user(self, account_id, status):
        if not self.urfa_call(0x2003):
            print "error calling function"
            return False
        
        print account_id
        packet = self.getPacket()
        packet.DataSetInt(account_id)
        packet.DataSetInt(status)
        self.urfa_send_param(packet)
        self.urfa_get_data()
    

    def rpcf_get_userinfo(self, user_id):
        data = {}
        if not self.urfa_call(0x2006):
            print "error calling function"
            return False
        packet = self.getPacket()
        packet.DataSetInt(user_id)
        self.urfa_send_param(packet)
        tmp = self.urfa_get_data()
        data['user'] = tmp.DataGetInt()
        if data['user'] != 0:
            data['accounts_count'] = tmp.DataGetInt()
            data['accounts'] = []
            for i in range(0, data['accounts_count']):
                account = {'id': tmp.DataGetInt(), 'name': tmp.DataGetString()}
                data['accounts'].append(account)
        data['login'] = tmp.DataGetString()
        data['password'] = tmp.DataGetString()
        data['basic_account'] = tmp.DataGetInt()
        data['full_name'] = tmp.DataGetString()
        data['create_date'] = tmp.DataGetInt()
        data['last_change_date'] = tmp.DataGetInt()
        data['who_create'] = tmp.DataGetInt()
        data['who_change'] = tmp.DataGetInt()
        data['is_juridical'] = tmp.DataGetInt()
        data['jur_address'] = tmp.DataGetString()
        data['act_address'] = tmp.DataGetString()
        data['work_tel'] = tmp.DataGetString()
        data['home_tel'] = tmp.DataGetString()
        data['mob_tel'] = tmp.DataGetString()
        data['web_page'] = tmp.DataGetString()
        data['icq_number'] = tmp.DataGetString()
        data['tax_number'] = tmp.DataGetString()
        data['kpp_number'] = tmp.DataGetString()
        data['bank_id'] = tmp.DataGetInt()
        data['bank_account'] = tmp.DataGetString()
        data['comments'] = tmp.DataGetString()
        data['personal_manager'] = tmp.DataGetString()
        data['connect_date'] = tmp.DataGetInt()
        data['email'] = tmp.DataGetString()
        data['is_send_invoice'] = tmp.DataGetInt()
        data['advance_payment'] = tmp.DataGetInt()
        data['house_id'] = tmp.DataGetInt()
        data['flat_number'] = tmp.DataGetString()
        data['entrance'] = tmp.DataGetString()
        data['floor'] = tmp.DataGetString()
        data['district'] = tmp.DataGetString()
        data['building'] = tmp.DataGetString()
        data['passport'] = tmp.DataGetString()
        data['parameters_count'] = tmp.DataGetInt()
        self.urfa_get_data()
        return data

    def rpcf_get_user_tariffs(self, user_id, account_id):  #0x3017
        data = {}
        if not self.urfa_call(0x3017):
            print "error calling function"
            return False
        packet = self.getPacket()
        packet.DataSetInt(user_id)
        packet.DataSetInt(account_id)
        self.urfa_send_param(packet)
        tmp = self.urfa_get_data()
        data['count'] = tmp.DataGetInt()
        data['tariffs'] = []
        for i in range(0, data['count']):
            tarif = {'current_tarif': tmp.DataGetInt(), 'next_tarif': tmp.DataGetInt(),
                     'discount_period_id': tmp.DataGetInt(), 'tarif_link_id': tmp.DataGetInt()}
            data['tariffs'].append(tarif)
        self.urfa_get_data()
        return data
