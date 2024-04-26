
import crypto

class classicWallet():
    def __init__(self) -> None:
        self.private_key = None,
        self.public_key = None,
        self.wallet_address = None,
        
    def generateWallet(self):
        self.private_key, self.public_key = crypto.eth_generate_keys()
        self.wallet_address = crypto.eth_public_key_to_address(self.public_key)


class quantumWallet():
    def __init__(self) -> None:
        self.private_key = None,
        self.public_key = None,
        self.wallet_address = None,
        
    def generateWallet(self):
        self.private_key, self.public_key = crypto.generate_keys()
        hash = (crypto.hash(self.public_key))
        self.wallet_address = hash[-20:]


if __name__ == '__main__':
    wallet_1 = classicWallet()
    wallet_1.generateWallet()

    print(len(wallet_1.private_key))
    print(len(wallet_1.public_key))
    print(len(wallet_1.wallet_address))