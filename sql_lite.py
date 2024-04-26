import sqlite3
import json

class SQLiteDB:
    def __init__(self, db_path):
        # Connect to SQLite database
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.connection.commit()

    def add(self, data_id, data):
        # Convert data to JSON string before storing in SQLite
        data_json = json.dumps(data)

        # Insert data into the SQLite database
        self.cursor.execute('''
            INSERT INTO data (id, value) VALUES (?, ?)
        ''', (data_id, data_json))
        self.connection.commit()

    def remove(self, data_id):
        # Remove data from SQLite database using the data_id
        self.cursor.execute('''
            DELETE FROM data WHERE id = ?
        ''', (data_id,))
        self.connection.commit()

    def get_all(self):
        # Retrieve all data from the SQLite database
        self.cursor.execute('SELECT * FROM data')
        rows = self.cursor.fetchall()
        return [{'id': row[0], 'value': json.loads(row[1])} for row in rows]

    def get_data_by_id(self, data_id):
        # Retrieve a specific data by its ID
        self.cursor.execute('SELECT * FROM data WHERE id = ?', (data_id,))
        row = self.cursor.fetchone()
        if row:
            return {'id': row[0], 'value': json.loads(row[1])}
        else:
            print(f"Data with ID {data_id} not found.")
            return None

    def close_db(self):
        # Close the SQLite database connection
        self.connection.close()


if __name__ == "__main__":

    # Example usage:
    mempool_sqlite = SQLiteDB("mempool_sqlite.db")

    # Add data to the SQLite mempool
    mempool_sqlite.add("tx1", {"from": "0xSender1", "to": "0xRecipient1", "value": 100})
    mempool_sqlite.add("tx2", {"from": "0xSender2", "to": "0xRecipient2", "value": 200})

    # Display current data in the SQLite mempool
    print("Current data in the SQLite mempool:")
    print(mempool_sqlite.get_all())

    ts = mempool_sqlite.get_all()

    for t in ts:
        print(t)

    print(t["value"])

    # Remove data from the SQLite mempool
    mempool_sqlite.remove("tx1")

    # Display updated data in the SQLite mempool
    print("\nData after removal:")
    print(mempool_sqlite.get_all())

    # Close the SQLite database connection when done
    mempool_sqlite.close_db()