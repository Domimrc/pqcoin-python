import plyvel
import json

class LevelDB:
    def __init__(self, db_path):
        # Open the LevelDB database
        self.db = plyvel.DB(db_path, create_if_missing=True)

    def add(self, data_id, data):
        # Convert transaction to JSON string before storing in LevelDB
        data_json = json.dumps(data)
        # Store the transaction in LevelDB with the transaction_id as the key
        self.db.put(data_id.encode('utf-8'), data_json.encode('utf-8'))

    def remove(self, data_id):
        # Remove the transaction from LevelDB using the transaction_id
        self.db.delete(data_id.encode('utf-8'))

    def get_all(self):
        data = []
        # Iterate through LevelDB to retrieve all transactions
        for key, value in self.db:
            data.append(json.loads(value.decode('utf-8')))
        return data
    
    def get_all_and_id(self):
        data = []
        id = []
        # Iterate through LevelDB to retrieve all transactions
        for key, value in self.db:
            data.append(json.loads(value.decode('utf-8')))
            id.append(key.decode('utf-8'))
        return id, data
    
    def get_data_by_id(self, data_id):
        # Retrieve a specific transaction by its ID
        value = self.db.get(data_id.encode('utf-8'))
        if value:
            return json.loads(value.decode('utf-8'))
        else:
            print(f"Data with ID {data_id} not found.")
            return None

    def close_db(self):
        # Close the LevelDB database
        self.db.close()


if __name__ == "__main__":

    # Example usage:
    mempool_leveldb = LevelDB("mempool_leveldb")

    # Add transactions to the LevelDB mempool
    mempool_leveldb.add("tx1", {"from": "0xSender1", "to": "0xRecipient1", "value": 100})
    mempool_leveldb.add("tx2", {"from": "0xSender2", "to": "0xRecipient2", "value": 200})

    # Display current transactions in the LevelDB mempool
    print("Current transactions in the LevelDB mempool:")
    print(mempool_leveldb.get_all())

    # Remove a transaction from the LevelDB mempool
    mempool_leveldb.remove("tx1")

    # Display updated transactions in the LevelDB mempool
    print("\nTransactions after removal:")
    print(mempool_leveldb.get_all())

    # Close the LevelDB database when done
    mempool_leveldb.close_db()