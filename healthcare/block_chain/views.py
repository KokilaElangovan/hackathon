from django.shortcuts import render
from django.conf import settings
from uuid import uuid4
from django.contrib.sessions.backends.db import SessionStore
from models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from block_chain.tests import Block, BlockChain, Record, Node
from rest_framework.response import Response
import os, json
import base64
import binascii
from Crypto.Cipher import AES

blocksize = 16
padding = '{'

def get_user_records(request):
    user_records=BlockChain().get_user_records(json.loads(request.body)['public_key'])
    return HttpResponse(json.dumps(user_records))

def new_record(request):
    data = json.loads(request.body)
    block = Block()
    record = Record(data['public_key'], data['personal_details'], data['medical_details'])
    block.add_record(record)
    print '-----------------------------------------------------'
    return HttpResponse(status=200)

def get_public_key(request):
    secret = os.urandom(blocksize)
    public_key = binascii.hexlify(secret)
    return HttpResponse(json.dumps({'public_key':public_key}))

def get_block_chain(request):
    block_chain = BlockChain().chain()
    return HttpResponse(json.dumps(block_chain))
