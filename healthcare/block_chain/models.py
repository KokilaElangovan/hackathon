# import hashlib
# import json
# from urlparse import urlparse
# import views
# import requests
# from django.conf import settings
# from bson.json_util import dumps, loads
# from root.dbconnections import MongoDB
# # Instantiate the Blockchain

# class Node:
#     def __init__(self):
#         self.nodes=set()
#         """
#         Set of nodes in the blockchain
#         """
#         # nodes = Fetch the list of all nodes from DB
#         if len(self.nodes) == 0:
#             self.register_node(settings.SELF_ADDRESS)

#     def register_node(self, address):
#         """
#         Add a new node to the list of nodes

#         :param address: Address of node. Eg. 'http://192.168.0.5:5000'
#         """

#         parsed_url = urlparse(address)
#         self.nodes.add(parsed_url.netloc)
#         views.notify(address=address)
#         self.save()

#     def get_all_nodes():
#         return list(self.nodes)

#     def save(self):
#         pass
#         # SAVE self.nodes into MongoDB

# class BlockChain:
#     def __init__(self):
#         self.latest_block = self.get_latest_block()

#     @property
#     def chain(self):
#         pass
#         #TODO Read the entire blockchain from MongoDB

#     def get_user_records(self, public_key):
#         pass
#         #Fetch all records with given public key

#     @staticmethod
#     def get_latest_block():
#         #TODO get the latest block from blockchain
#         db = MongoDB().connect()
#         latest_block = dumps(db.find().sort({"_id",-1}).limit(1))
#         return loads(latest_block)[0]

#     def validate_chain(self, chain):
#         """
#         Determine if a given blockchain is valid

#         :param chain: A blockchain
#         :return: True if valid, False if not
#         """

#         last_block = chain[0]
#         current_index = 1

#         while current_index < len(chain):
#             block = chain[current_index]
#             print(last_block)
#             print(block)
#             print("\n-----------\n")
#             # Check that the hash of the block is correct
#             if block['previous_hash'] != Block.hash(last_block):
#                 return False

#             # Check that the Proof of Work is correct
#             # if not self.valid_proof(last_block['proof'], block['proof']):
#             #     return False

#             last_block = block
#             current_index += 1

#         return True

#     def resolve_conflicts(self):
#         """
#         Consensus algorithm: it resolves conflicts
#         by replacing our chain with the longest one in the network.

#         :return: True if our chain was replaced, False if not
#         """
#         node_obj = Node()
#         neighbours = node_obj.nodes
#         new_chain = None

#         # We're only looking for chains longer than ours
#         max_length = len(self.chain)

#         # Grab and verify the chains from all the nodes in our network
#         for node in neighbours:
#             response = requests.get('http://'+node+'/chain')

#             if response.status_code == 200:
#                 length = response.json()['length']
#                 chain = response.json()['chain']

#                 # Check if the length is longer and the chain is valid
#                 if length > max_length and self.validate_chain(chain):
#                     max_length = length
#                     new_chain = chain

#         # Replace our chain if we discovered a new, valid chain longer than ours
#         if new_chain:
#             self.chain = new_chain
#             return True

#         return False

# blockchain = BlockChain()

# class Block:

#     def new_block(self, record, previous_hash):
#         block = {
#             'id': self.latest_block_id + 1,
#             'previous_hash': previous_hash if previous_hash else self.previous_block_hash(),
#             'records': [record]
#         }
#         blockchain.latest_block = block

#         return block
        
#     def previous_block_hash():
#         #TODO Take the latest block and hash it
#         # hash function is available below
#         pass
#         #TODO

#     @property
#     def latest_block_id(self):
#         return blockchain.get_latest_block().get('_id')

#     def add_record(self, record):
#         if len(blockchain.latest_block['records']) <= settings.MAX_RECORDS:
#             new_block = self.new_block(record=record)
#         else:
#             new_block = blockchain.get_latest_block()['records'].update(record)

#         self.save(new_block)
#         notify(record=record.get_record_as_json())

#     def save(block):
#         pass
#         #TODO: Insert if not exists, the block into the MongoDB - Upsert

# class Record:
#     def __init__(self, public_key, personal_details, medical_details):
#         self.id = self.previous_record_id() + 1
#         self.public_key = public_key
#         self.previous_hash = self.previous_record_hash
#         self.personal_details = self.encrypt(personal_details)
#         self.medical_details = medical_details

#     def get_record_as_json(self):
#         #self will be a Record class object
#         # properties u will get as record.id , record. public_key etc.
#         # Convert to JSON
#         pass
#         # convert values from self and convert it as a json

#     @staticmethod
#     def encrypt(data):
#         pass
#         #TODO encrypt the data to send

#     @property
#     def previous_record_hash(self):
#         latest_block = blockchain.get_latest_block()
#         return hash(latest_block['records'][-1])

#     @property
#     def last_block(self):
#         return self.chain[-1]


#     @staticmethod
#     def hash(data):
#         """
#         Creates a SHA-256 hash of a Block

#         :param block: Block
#         """

#         # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
#         block_string = json.dumps(data, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()

#     def proof_of_work(self, last_proof):
#         """
#         Simple Proof of Work Algorithm:
#          - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
#          - p is the previous proof, and p' is the new proof
#         """

#         proof = 0
#         while self.valid_proof(last_proof, proof) is False:
#             proof += 1

#         return proof

#     @staticmethod
#     def valid_proof(last_proof, proof):
#         """
#         Validates the Proof

#         :param last_proof: Previous Proof
#         :param proof: Current Proof
#         :return: True if correct, False if not.
#         """

#         guess = last_proof[proof].encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash[:4] == "0000"