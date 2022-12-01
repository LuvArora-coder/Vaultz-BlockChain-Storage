import hashlib
import json

class Block:
    def __init__(self, index, timestamp, documents, previous_hash = ''):
        self.index = index
        self.documents = documents
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        return str(
            hashlib.sha256(
                str(str(self.index) + str(json.dumps(self.documents)) + str(self.timestamp) + str(self.previous_hash)).encode()
            ).hexdigest()
        )
    
    def serialize(self):
        data = {
            'i': self.index,
            't': self.timestamp,
            'd': self.documents,
            'p': self.previous_hash,
            'h': self.hash
        }
        return data