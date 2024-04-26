from flask import Flask, jsonify, request

from transaction import Tx
import network_setup

import sqlite3
import sql_lite
import requests
import threading


app = Flask(__name__)



#Request Key
@app.route('/verify_tx', methods=['POST']) 
def verify_tx(slave_SAE_ID):
    """XXXXX
    """

    port_number = request.environ['SERVER_PORT']

    print(f"(EXE) {port_number}: Received Tx")

     # Access POST data from the request body (assuming it's JSON data)
    data = request.json  # This assumes that the data sent is in JSON format and returns a dict

    print(f"(EXE) {port_number}: Data recived {data} data")
    
    if data is None:
        response = jsonify({"message": "Invalid JSON data"})
        response.status_code = 400
        return response
    
    tx_received = Tx()
    tx_received.set_from_dict(data)
    
    #verify Transaction
    if tx_received.is_valid():
        print(f"(EXE) {port_number}: Tx is valid")

        tx_received.add_tx_to_mempool("mempool.db")

        conn = sqlite3.connect('network_config.db')
        cursor = conn.cursor()

        nodes = sql_lite.get_all_nodes(cursor)

        for node in nodes:
            url = f"http://{network_setup.NETWORK}:{node[1]}/add_tx_to_mempool"
            r = requests.post(url, data, headers={'Content-Type': 'application/json'})
    
    else:
        print(f"(EXE) {port_number}: Tx is NOT valid")

def mining():
    #Load TxList

    conn = sqlite3.connect('mempool.db')
    cursor = conn.cursor()

    txs = sql_lite.get_all_tx(cursor)

    for tx in txs:




def run(PORT):
    print(f'Running Execution_client on Port {PORT}')

    parallel_thread = threading.Thread(target=mining, args=())
    parallel_thread.daemon = True
    parallel_thread.start()

    
    # Set a variable in the app's config
    app.config['node_nr'] = node_nr
    app.config['databases'] = network_setup.DATABASES
    #app.run(ssl_context=('localhost_cert.pem', 'localhost_key.pem'), debug=False, port=PORT)
    app.run(debug=False, port=PORT)