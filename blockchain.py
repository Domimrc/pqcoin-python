from cryptography.hazmat.primitives import hashes

import json
import os
import time


from eth_keys import keys
from eth_keys.backends import NativeECCBackend
from eth_utils import keccak
from rlp import encode, decode



# Function to load the existing blockchain from a file
def load_blockchain_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

# Function to save the blockchain to a file
def save_blockchain_to_file(filename, blockchain):
    with open(filename, 'w') as file:
        json.dump(blockchain, file, indent=2)



def sign_transaction(transaction, private_key):
        # Convert private key hex to bytes
        private_key = keys.PrivateKey(private_key)

        transaction_list = list(transaction.items())

        # Create a transaction hash
        transaction_hash = keccak(encode(transaction_list))

        # Sign the hash with the private key
        signature = keys.ecdsa_sign(transaction_hash, private_key)

        # Construct r, s, and v values
        r, s, v = signature.vrs

        # Add the signature to the transaction
        transaction['r'] = r
        transaction['s'] = s
        transaction['v'] = v

        return transaction


# Function to calculate the hash of a block
def calculate_block_hash(new_block):
    #block = encode([block['rawTransactions'], block['parentHash'], block['number'], block['nonce'], block['difficulty']])
    # Convert the dictionary to a JSON-formatted string
    block_json = json.dumps(new_block, sort_keys=True)

    # Calculate the SHA-256 hash
    #block_hash = hashlib.sha256(block_json.encode()).hexdigest()
    return keccak(block_json.encode()).hex()

# Function to mine a block with a given difficulty target
def mine_block(block):
    difficulty = block['difficulty']
    while True:
        block['nonce'] += 1
        block_hash = calculate_block_hash(block)
        if int(block_hash, 16) < 2**(256 - difficulty):
            block['hash'] = block_hash
            return block



if __name__ == "__main__":

    # Replace '0xYourSenderAddress' and '0xYourPrivateKey' with the actual sender address and private key
    sender_address = '0xYourSenderAddress'
 
    private_key = b'0xYourPrivateKey0xYourPrivateKey'
  

    # Replace '0xRecipientAddress' with the actual recipient address
    recipient_address = '0xRecipientAddress'

    # Create a simple transaction
    transaction = {
        'nonce': 0,
        'gasPrice': 30000000000,  # 30 Gwei in Wei
        'gas': 21000,
        'to': recipient_address,
        'value': 1000000000000000000,  # 1 Ether in Wei
        'data': '',
    }

    # Sign the transaction
    signed_transaction = sign_transaction(transaction, private_key)
    # add hash to transaction
    signed_transaction['hash']=keccak(encode(list(signed_transaction.items()))).hex()

    print("signed_transaction", signed_transaction)

    #----------------------------------------------------------------

    rawTransactions = []
    rawTransactions.append(signed_transaction)

    print("rawtransactions", rawTransactions)


    # Convert the result to a dictionary for better readability
    new_block = {
        'number': 1,
        'parentHash' : "parentHash1",
        'rawTransactions': rawTransactions,
        'nonce': 0,
        'difficulty': 18,  # Replace with the actual difficult
    }

    print(json.dumps(new_block, indent=2))
    

    # Mine the block
    mined_block = mine_block(new_block)

    print(json.dumps(mined_block, indent=2))


    # Save the mined block to the blockchain file
    blockchain_filename = 'blockchain.json'
    blockchain = load_blockchain_from_file(blockchain_filename)
    blockchain.append(mined_block)
    save_blockchain_to_file(blockchain_filename, blockchain)

    # Print the blockchain
    print(json.dumps(blockchain, indent=2))