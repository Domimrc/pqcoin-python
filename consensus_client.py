from flask import Flask, jsonify, request
import threading
import sqlite3
from sql_lite import SQLiteDB
import json

import sql_lite
import blockchain
import time

app = Flask(__name__)


#Key Request from Quantum Node 1
@app.route('/<int:Master_KME_ID>/req_key', methods=['POST'])
def req_key(Master_KME_ID):
    """Returns Key container data from the KME to the calling slave SAE. Key container data
    contains one or more keys. The slave SAE specified by the slave_SAE_ID
    parameter may subsequently request matching keys from a remote KME using key_ID
    identifiers from the returned Key container.
    """

    print(f"(CP) received request from Master_Node for control plane from Node", Master_KME_ID)


def mining():

    difficult = 18
    number = 0
    parentHash = "Genesis"

    while True:
        mempool = SQLiteDB("mempool_sqlitedb")
        txs = mempool.get_all()
        mempool.close_db()

        rawTransactions = []

        for tx in txs:
            rawTransactions.append(tx["value"])

        #print("rawtransactions", rawTransactions)

        # Convert the result to a dictionary for better readability
        new_block = {
            'number': number ,
            'parentHash' : parentHash ,
            'rawTransactions': rawTransactions,
            'nonce': 0,
            'difficulty': difficult,  # Replace with the actual difficult
        }

        #print(json.dumps(new_block, indent=2))
        start_time = time.time()

        # Mine the block
        mined_block = blockchain.mine_block(new_block)

        end_time = time.time()

        print(json.dumps(mined_block, indent=2))


        # Save the mined block to the blockchain file
        blockchain_filename = 'blockchain.json'
        blockchain_ = blockchain.load_blockchain_from_file(blockchain_filename)
        blockchain_.append(mined_block)
        blockchain.save_blockchain_to_file(blockchain_filename, blockchain_)

        # Print the blockchain
        print(json.dumps(blockchain_, indent=2))

        mempool = SQLiteDB("mempool_sqlitedb")
        for tx in txs:
            #print(id)
            mempool.remove(tx["id"])
        mempool.close_db()


        if (end_time - start_time) < 5:
            difficult+=1
        else:
            difficult-=1

        number +=1
        parentHash= mined_block['hash']




def run(port):

    parallel_thread = threading.Thread(target=mining, args=(status,))
    parallel_thread.daemon = True
    parallel_thread.start()

    #app.run(ssl_context=('localhost_cert.pem', 'localhost_key.pem'), debug=False, port=port)
    app.run( debug=False, port=port)


if __name__ == "__main__":
    mining()