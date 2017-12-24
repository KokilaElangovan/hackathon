from django.shortcuts import render
from django.conf import settings
from uuid import uuid4
from django.contrib.sessions.backends.db import SessionStore
from models import blockchain, node, Block, Record

# Instantiate the Node
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
initial_node = False

#Move the IP checking to decorators
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def notify(address=False, record=False):
    global initial_node
    initial_node = True
    # notify all other nodes
    node_list = node.get_all_nodes()
    next_node = node_list[node_list.index(settings.SELF_ADDRESS) + 1]
    data = get_notification_data('address', address) if address else get_notification_data('record', record)
    r = requests.post(f'http://{next_node}/notify', data=data)

def get_notification_data(notification_type, data):
    return {
        'type': notification_type,
        'data': data
    }

def get_notified(request):
    global initial_node
    if initial_node:
        initial_node = False
    else:
        post_data = request.POST.get('data')
        if post_data.get('type') == 'address':
            notify(address=post_data.get('data'))
        elif post_data.get('type') == 'node':
            record = post_data.get('data')
            block = Block()
            block.add_record(Record(record['public_key'], record['personal_details'], record['medical_details']))
            notify(record=record)


def new_record(request):
    data = request.POST.get('data')

    # Check that the required fields are in the POST'ed data
    required = ['public_key', 'personal_details', 'medical_details']
    if not all(k in data for k in required):
        return 'Missing values', 400
    add.record(data.get('public_key'), data.get('personal_detail'), data.get('medical_detail'))


    #TODO
    response = blockchain.get_user_records(data.get('public_key'))
    return HttpResponse(json.dumps(response), mimetype="application/json")

def join_request(request):
    ip = get_ip(request)
    node.register_node(ip)
    notify(address=ip)
    return HttpResponse(json.dumps(blockchain.chain),  mimetype="application/json")

def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


def consensus():
    replaced = blockchbain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# if __name__ == '__main__':
#     from argparse import ArgumentParser

#     parser = ArgumentParser()
#     parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
#     args = parser.parse_args()
#     port = args.port

#     app.run(host='0.0.0.0', port=port)
