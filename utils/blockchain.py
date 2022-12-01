from utils.block import Block
import time
import json
import threading
import hashlib

class Blockchain():
    def __init__(self):
        self.chain = []
        self.waiting_documents = []
        self.difficulty = 4
        self.load_chain_from_file()
    
    def get_recent_block_hash(self):
        if len(self.chain) == 0:
            return ''
        else:
            return self.chain[-1].hash

    def append_document(self, document):
        self.waiting_documents.append(document.serialize())

    def mine(self):
        i = 0
        while True:
            i += 1
            if len(self.waiting_documents) > 0:
                data = self.waiting_documents
                block = Block(len(self.chain) + 1, int(time.time()), data, self.get_recent_block_hash())
                
                digest = hashlib.sha256((block.hash + str(i)).encode()).hexdigest()

                if digest[:self.difficulty] == ('0' * self.difficulty):
                    print('PoW result: ' + digest + ' for block #' + str(block.index))
                    self.chain.append(block)
                    self.waiting_documents = self.waiting_documents[:-1]
                    self.save_chain_to_file()
    
    def start_mining(self):
        thread = threading.Thread(target=self.mine)
        thread.start()
    
    def save_chain_to_file(self):
        f = open('static\chain.json', 'w')
        f.write(json.dumps(self.dump_chain()))
        f.close()

    def load_chain_from_file(self):
        try:
            f = open('static\chain.json', 'r')
            raw_chain = json.loads(f.read())

            print('Loading chain from file...')

            for b in raw_chain:
                block = Block(b['i'], b['t'], b['d'], b['p'])
                if b['h'] == block.hash:
                    self.chain.append(block)
                else:
                    print('Inconsistent data in chain.json')
                    exit(1)
            f.close()
        except Exception as e:
            print(e)
            print('Cannot load chain from file, creating empty instead...')

    def look_for_document_by_checksum(self, checksum):
        for block in self.chain:
            for doc in block.documents:
                if doc['c'] == checksum:
                    return {
                        'block': block,
                        'doc': doc
                    }
        return None

    def get_block_by_hash(self, hash):
        for block in self.chain:
            if block.hash == hash:
                return block
        return None

    def dump_chain(self):
        return [b.serialize() for b in self.chain]