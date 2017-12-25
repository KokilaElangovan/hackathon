from django.test import TestCase

# Create your tests here.
import hashlib
import json
from urlparse import urlparse
import views
import requests
from django.conf import settings
from bson.json_util import dumps, loads
from root.dbconnections import MongoDB

class Node:
    def __init__(self):
        self.nodes=set()
        """
        Set of nodes in the blockchain
        """
        # nodes = Fetch the list of all nodes from DB
        if len(self.nodes) == 0:
            self.register_node(settings.SELF_ADDRESS)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        views.notify(address=address)
        self.save()

    def get_all_nodes():
        return list(self.nodes)

    def save(self):
        pass
        # SAVE self.nodes into MongoDB


class Block:

    def new_block(self):
        block = {
            '_id': self.latest_block_id + 1,
            'previous_hash': self.previous_block_hash(),
        }
        self.save_block(block)
        
    def previous_block_hash(self):
        BlockChain.get_latest_block().get('previous_block_hash', 'previous_block_hash')

    @property
    def latest_block_id(self):
        return BlockChain.get_latest_block().get('_id', 0)

    def add_record(self, record):
        blockchain = BlockChain.get_latest_block()
        if 'records' in blockchain.keys() and len(blockchain['records']) <= 3:
            self.save_record(BlockChain.get_latest_block(), record)
        else:
            self.new_block()
            self.save_record(BlockChain.get_latest_block(), record)

    def save_block(self, block):
        db = MongoDB().connect()
        db.insert(block)

    def save_record(self, block, record):
        db = MongoDB().connect()
        record = {'id': record.id, 'public_key':record.public_key, 'previous_record_hash':record.previous_record_hash, 'personal_details':record.personal_details, 'medical_details':record.medical_details}
        db.update({'_id':block['_id']},{'$push' : {'records' : record}})

class Record:
    def __init__(self, public_key, personal_details, medical_details):
        self.id = self.latest_record_id() + 1
        self.public_key = public_key
        self.previous_hash = self.previous_record_hash
        self.personal_details = personal_details
        self.medical_details = medical_details

    def get_record_as_json(self):
        #self will be a Record class object
        # properties u will get as record.id , record. public_key etc.
        # Convert to JSON
        pass
        # convert values from self and convert it as a json

    def latest_record_id(self):
        latest_block = BlockChain.get_latest_block()
        if 'records' in latest_block.keys():
            return latest_block['records'][-1]['id']
        else:
            return 0

    @staticmethod
    def encrypt(data):
        pass
        #TODO encrypt the data to send
    
    @staticmethod
    def hashme(msg):
        if type(msg)!=str:
            msg = json.dumps(msg)
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

    @property
    def previous_record_hash(self):
        latest_block = BlockChain.get_latest_block()
        if 'records' in latest_block.keys():
            return self.hashme(latest_block['records'][-1])
        return self.hashme('example_data')

    @property
    def last_block(self):
        return self.chain[-1]


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof

        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        """

        guess = last_proof[proof].encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


class BlockChain:
    def __init__(self):
        self.latest_block = self.get_latest_block()

    @property
    def chain(self):
        pass
        #TODO Read the entire blockchain from MongoDB

    def get_user_records(self, public_key):
        db = MongoDB().connect()
        records=json.loads(dumps(db.find()))
        user_records = []
        for block in range(1,records[-1]['_id']):
            for record in records[block]['records']:
              if record['public_key'] == public_key:
                record['personal_details'] = decryption(public_key, record['personal_details'])
                user_records.append(record)
        return user_records

    @staticmethod
    def get_latest_block():
        db = MongoDB().connect()
        latest_block = json.loads(dumps(db.find().sort("_id",-1).limit(1)))
        if len(latest_block) > 0:
            return latest_block[0]
        else :
            return {}
    def decryption(secret, data):
        secret = binascii.unhexlify(secret)
        DecodeAES = lambda c, e : c.decrypt(base64.b64decode(e)).rstrip(padding)
        cipher = AES.new(secret)
        decode = DecodeAES(cipher, data)
        return decode

    def validate_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            if block['previous_hash'] != Block.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            # if not self.valid_proof(last_block['proof'], block['proof']):
            #     return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Consensus algorithm: it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """
        node_obj = Node()
        neighbours = node_obj.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://'+node+'/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.validate_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False