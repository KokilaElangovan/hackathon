from __future__ import unicode_literals

from django.db import models

import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests
from django.conf import settings

address = settings.SELF_ADDRESS
# Instantiate the Blockchain
blockchain = Blockchain()

class Node():
    def __init__(self):
        nodes=set()
        """
        Set of nodes in the blockchain
        """
        # nodes = Fetch the list of all nodes from DB
        if len(nodes) == 0:
            self.register_node(address)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

class BlockChain():
    def __init__(self):
        self.last_block = get_last_block()

    @property
    def chain(self):
        #TODO Read the entire blockchain from MongoDB

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
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
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
            response = requests.get(f'http://{node}/chain')

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


class Block:
    def new_block(self, record, previous_hash):
        block = {
            'id': self.last_block_id + 1,
            'previous_hash': previous_hash if previous_hash else self.previous_block_hash(),
            'records': [record]
        }
        blockchain.last_block = block
        #TODO Save the new_block in MongoDB

        return block
        
    @staticmethod
    def get_last_block():
        #TODO Read the last block from MongoDB and return

    @property
    def last_block_id(self):
        return self.get_last_block().get('id')


    def add_record(self, record):
        if len(blockchain.last_block['records']) == settings.MAX_BLOCKS:
            new_block = self.new_block(record=record)
        # Save new_block into MongoDB


class Record:
    def __init__(self, public_key, personal_details, medical_details):
        self.id = self.last_record_id() + 1
        self.public_key = public_key
        self.previous_hash = self.previous_record_hash
        self.personal_details = personal_details
        self.medical_details = medical_details

    @property
    def previous_record_hash(self):
        # Get the last block
        last_block = Block.get_last_block()
        if len(last_block.transactions[-1]) > 0:
            return self.hash(transactions)

    @property
    def last_block(self):
        return self.chain[-1]


    @staticmethod
    def hash(data):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    #Commenting for now. Yet to finalize if needed
    # def proof_of_work(self, last_proof):
    #     """
    #     Simple Proof of Work Algorithm:
    #      - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
    #      - p is the previous proof, and p' is the new proof
    #     """

    #     proof = 0
    #     while self.valid_proof(last_proof, proof) is False:
    #         proof += 1

    #     return proof

    # @staticmethod
    # def valid_proof(last_proof, proof):
    #     """
    #     Validates the Proof

    #     :param last_proof: Previous Proof
    #     :param proof: Current Proof
    #     :return: True if correct, False if not.
    #     """

    #     guess = f'{last_proof}{proof}'.encode()
    #     guess_hash = hashlib.sha256(guess).hexdigest()
    #     return guess_hash[:4] == "0000"