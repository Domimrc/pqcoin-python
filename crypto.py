#cryptography.py

from cryptography.hazmat.primitives import hashes

import base64
import secrets
import binascii

from eth_keys import keys


import oqs

#sigalg = 'SPHINCS+-SHA256-256s-robust'
#sigalg = 'Dilithium3'
sigalg = 'Falcon-512'

def generate_keys():
    signer=oqs.Signature(sigalg)
    pu_ser = signer.generate_keypair() #byte
    private = signer.export_secret_key()  #byte
    return private, pu_ser #public key serialized


def eth_generate_keys():
    # Specify the length of the bytes string
    length = 32

    # Generate a random bytes string
    random_bytes = secrets.token_bytes(length)

    pk = keys.PrivateKey(random_bytes)
    pu = pk.public_key
    return pk, pu

def eth_public_key_to_address(pu):
    addr_byte = pu.to_canonical_address()
    return binascii.hexlify(addr_byte).decode('utf-8')


def eth_sign(pk,messeage_in_byte):
    signature = pk.sign_msg(messeage_in_byte)
    return signature

def eth_verify(pu, signature, messeage_in_byte):
    return signature.verify_msg(messeage_in_byte, pu)


def eth_public_key_recovery(signature, messeage_in_byte):
    pu_rec = signature.recover_public_key_from_msg(messeage_in_byte)
    return pu_rec


def sign(message, private):
    #calculate Hash and generate signature with ECDSA and curve defined in private key
    message = bytes(str(message), 'utf8')
    #sig = private.sign(message, ec.ECDSA(hashes.SHA3_256())
    signer = oqs.Signature(sigalg,private)
    sig = signer.sign(message)
    return sig

def verify (message, sig, pu_ser):
    try:
        verifier=oqs.Signature(sigalg)
        message = bytes(str(message), 'utf8')
        correct = verifier.verify(message, sig, pu_ser)
        return correct
    except:
        print("Error executing public_key.verify")
        return False

def hash(value):
    digest = hashes.Hash(hashes.SHA3_256())
    digest.update(bytes(str(value),'utf8'))
    #digest.update(bytes(str(value),'utf8'))
    hash = digest.finalize()
    return hash

def savePrivate(pr_key, filename):    
    fp = open(filename, "wb")
    fp.write(pr_key)
    fp.close()
    return 

def loadPrivate(filename):
    fin = open(filename, "rb")
    pr_key = fin.read()
    fin.close()
    return pr_key

def savePublic(pu_key, filename):
    pem = base64.b64encode(pu_key)
    pu_key_str= pem.decode("utf-8")
    fp = open(filename, "w")
    fp.write(pu_key_str)
    fp.close()
    return True

def loadPublic(filename):
    fin = open(filename, "r")
    pu_key_str = fin.read()
    fin.close()
    pem = pu_key_str.encode("utf-8")
    pu_key = base64.b64decode(pem)
    return pu_key

def loadKeys(pr_file, pu_file):
    return loadPrivate(pr_file), loadPublic(pu_file)


if __name__== '__main__':
    signer=oqs.Signature(sigalg)
    pu = signer.generate_keypair() #byte
    pr = signer.export_secret_key()  #byte

    #print("public key (bytes):", pu)
    #print("private key (binary):", pr)

    print("public key lenght (bytes):", len(pu))
    print("private key lenght (bytes):", len(pr))

    sig = sign("This is a secret message", pr)

    print("signature lenght (bytes):", len(sig))

    result = verify("This is a secret message", sig,pu)

    print("Verification", result)

    import sys
    pr, pu = eth_generate_keys()
    print(pr, pu, "not Bytes ( 1/2)")

    print(eth_public_key_to_address(pu))