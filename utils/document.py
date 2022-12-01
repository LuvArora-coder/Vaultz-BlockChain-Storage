import json

class Document():
    def __init__(self, checksum, description):
        self.checksum = checksum
        self.description = description
    
    def serialize(self):
        data = {
            'c': self.checksum,
            'd': self.description
        }

        return data