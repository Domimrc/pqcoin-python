#Transaction.py

import crypto
import json
import base64

import sqlite3
import sql_lite

from eth_utils import keccak
from rlp import encode, decode


def b64(bytesobject):
    return base64.b64encode(bytesobject).decode('utf-8')

def reverse_b64(encoded_string):
    return base64.b64decode(encoded_string.encode('utf-8'))


def genTx (nonce, recipient_address,value, data = ''):
    transaction = {
        'nonce': nonce,
        'gasPrice': 30000000000,  # 30 Gwei in Wei
        'gas': 21000,
        'to': recipient_address,
        'value': (value * 1000000000000000000),  # 1 Ether in Wei
        'data': data,
    }
    return transaction

# Sign the transaction
def sign_transaction(transaction, private_key):
        
        transaction_list = list(transaction.items())

        # Create a transaction hash
        transaction_hash = keccak(encode(transaction_list))

        # Sign the hash with the private key
        signature = crypto.eth_sign( private_key, transaction_hash)

        # Construct r, s, and v values
        r, s, v = signature.vrs

        # Add the signature to the transaction
        transaction['r'] = r
        transaction['s'] = s
        transaction['v'] = v

        transaction['hash']=keccak(encode(list(transaction.items()))).hex()

        return transaction


class Tx:
    def __init__(self)-> None:
        self.sender = None #public key
        self.recipient= None #addr
        self.value = None
        self.data = None
        self.gasLimit = None
        self.gasPrice = None
        self.signature = None

    def add_input(self, from_pu, to_addr, amount, data = None, gaslimit = 21000, gasprice = 100000): #from, to, value, gaslimit, gasprice 100000 for 2,1 mining rewarde, data
        
        self.recipient = to_addr
        self.value = amount
        self.gasLimit = gaslimit
        self.gasPrice = gasprice
        self.data = data
        self.sender = from_pu   

    def sign(self, private):
        message = self.__gather()
        newsig = crypto.sign(message, private)
        self.signature = newsig   

    def is_valid(self):
        #total_in = 0
        #total_out = 0
        message = self.__gather()
        #input check
        #for pu in self.sender: 
        found = False
        if crypto.verify(message, self.signature, self.sender):
            found = True
        if not found:
            return False
            #if amount < 0: #no negative values
            #    return False
            #total_in = total_in + amount
        #reqd check        
        #for addr in self.reqd:
        #    found = False
        #    for s in self.sigs:
        #        if Cryptography.verify(message, s, addr):
        #            found = True
        #    if not found:
        #        return False
        #output check
        #for amount in self.value:
        if self.value < 0: #no negative values
            return False
        #total_out = total_out + amount
        #total amount check
        #if total_out > total_in:
        #   return False

        return True
    
    def create_json(self):

        # a Python object (dict):
        #x = {"number": self.number,
        #     "size": self.size}
        x = {}

        x["sender"] = b64(self.sender)
        x["recipient"] = b64(self.recipient)
        x["value"] = self.value
        x["data"] = self.data
        x["gasLimit"] = self.gasLimit
        x["gasPrice"] = self.gasPrice
        x["signature"] = b64(self.signature)

        # convert into JSON:
        return json.dumps(x)
    
    def set_from_dict(self, data):
        self.sender = reverse_b64(data["sender"])
        self.recipient  = reverse_b64(data["recipient"])
        self.value = data["value"]
        self.data  = data["data"]
        self.gasLimit = data["gasLimit"]
        self.gasPrice  = data["gasPrice"]
        self.signature = reverse_b64(data["signature"])


    def add_tx_to_mempool(self, mempool):
        conn = sqlite3.connect(mempool)
        # Create a cursor object
        cursor = conn.cursor()
        sql_lite.insert_tx(cursor, conn, self.from_pu, self.to_addr, self.amount, self.data, self.gaslimit, self.gasprice)


    def __gather(self):
        tx_data=[]
        tx_data.append(self.recipient)
        tx_data.append(self.value)
        tx_data.append(self.data)
        tx_data.append(self.gasLimit)
        tx_data.append(self.gasPrice)
        tx_data.append(self.sender)
        return tx_data

    def __repr__(self): #representation
        #reprstr = "RECIPIENT:\n"
        #for to_addr in self.recipient:
        #    reprstr = reprstr + str(to_addr) + "\n"
        #reprstr = reprstr + "SENDER:\n"
        #for from_addr in self.sender:
        #    reprstr = reprstr + str(from_addr) + "\n"
        #reprstr = reprstr + "VALUE:\n"
        #for v in self.value:
        #    reprstr = reprstr + str(v) + "\n"
        #reprstr = reprstr + "DATA:\n"
        #for d in self.data:
        #    reprstr = reprstr + str(d) + "\n"
        #reprstr = reprstr + "gasLimit:\n"
        #for gl in self.gasLimit:
        #    reprstr = reprstr + str(gl) + "\n"
        #reprstr = reprstr + "gasPrice:\n"
        #for gp in self.gasPrice:
        #    reprstr = reprstr + str(gp) + "\n"
        #reprstr = reprstr + "END:\n"
        #return reprstr

        return "RECIPIENT:" + str(self.recipient) + "\n" + "SENDER:" + str(self.sender) + "\n" + "VALUE:" + str(self.value) + "\n" + "DATA:" + str(self.data) + "\n" + "gasLimit:" + str(self.gasLimit) + "\n" + "gasPrice:" + str(self.gasPrice) + "\n" + "signature:" + str(self.signature) + "\n" + "END:\n"
        




if __name__ == "__main__":
    #pr1, pu1 = Cryptography.generate_keys()
    #pr2, pu2 = Cryptography.generate_keys()
    #pr3, pu3 = Cryptography.generate_keys()
    #pr4, pu4 = Cryptography.generate_keys()

    pr1, pu1, addr1 = Cryptography.generateWallet()
    pr2, pu2, addr2 = Cryptography.generateWallet()
    
    print('addr1',addr1)
    addr11= Cryptography.getWalletAddr(pu1)
    print('addr11',addr11)

#ETHEREUM FORMAT 
    

    n=1 #counter
#RIGHT TRANSACTIONS
    #send 1 from person 1 to person 2
    Tx1 = Tx()
    Tx1.add_input(pu1, addr2, 1) #from, to, value, gaslimit, gasprice, data
    Tx1.sign(pr1)
    #print('TX',Tx1)

    #Tx1 = Tx()
    #Tx1.add_input(pu1, 1) 
    #Tx1.add_output(pu2, 1)
    #Tx1.sign(pr1)

    #send 1 from person 1 to person 2 and person 3
    #Tx2 = Tx()
    #Tx2.add_input(pu1, 2)
    #Tx2.add_output(pu2, 1)
    #Tx2.add_output(pu3, 1)
    #Tx2.sign(pr1)

    #send 1.1 from person 3 to person 1 and person 3 (with excrow 3rd party requirement)
    #Tx3 = Tx()
    #Tx3.add_input(pu3, 1.2)
    #Tx3.add_output(pu1, 1.1)
    #Tx3.add_reqd(pu4)
    #Tx3.sign(pr3)
    #Tx3.sign(pr4)

    for t in [Tx1]:
        if t.is_valid():
            print(n, "Success! Tx is valid")
        else:
            print(n, "ERROR! Tx is invalid")
        n=n+1

    

#WRONG TRANSACTIONS
    # Wrong signatures
    Tx4 = Tx()
    Tx4.add_input(pu1, addr2, 1) #from, to, value, gaslimit, gasprice, data
    Tx4.sign(pr2)

    #Tx4 = Tx()
    #Tx4.add_input(pu1, 1)
    #Tx4.add_output(pu2, 1)
    #Tx4.sign(pr2)

    # Escrow Tx not signed by the arbiter
    #Tx5 = Tx()
    #Tx5.add_input(pu3, 1.2)
    #Tx5.add_output(pu1, 1.1)
    #Tx5.add_reqd(pu4)
    #Tx5.sign(pr3)

    # Two input addrs, signed by one
    #Tx6 = Tx()
    #Tx6.add_input(pu3, 1)
    #Tx6.add_input(pu4, 0.1)
    #Tx6.add_output(pu1, 1.1)
    #Tx6.sign(pr3)

    # Outputs exceed inputs
    #Tx7 = Tx()
    #Tx7.add_input(pu4, 1.2)
    #Tx7.add_output(pu1, 1)
    #Tx7.add_output(pu2, 2)
    #Tx7.sign(pr4)

    # Negative values
    Tx8 = Tx()
    Tx8.add_input(pu1, addr2, -1) #from, to, value, gaslimit, gasprice, data
    Tx8.sign(pr1)

    #Tx8 = Tx()
    #Tx8.add_input(pu2, -1)
    #Tx8.add_output(pu1, -1)
    #Tx8.sign(pr2)

    # Modified Tx
    Tx9 = Tx()
    Tx9.add_input(pu1, addr2, 1) #from, to, value, gaslimit, gasprice, data
    Tx9.sign(pr1)

    Tx9.value = 2

    #print(Tx9)

    #Tx9 = Tx()
    #Tx9.add_input(pu1, 1)
    #Tx9.add_output(pu2, 1)
    #Tx9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    #Tx9.outputs[0] = (pu3,1)
    
    for t in [Tx4, Tx8, Tx9]:
        
        if t.is_valid():
            print(n, "ERROR! Bad Tx is valid")
        else:
            print(n, "Success! Bad Tx is invalid")
        n=n+1
    
        

    
        




    
    
        
