import sys

sys.path.append("..")

import app

probe_bc = app.blockchain.Blockchain()

print("index = {}".format(probe_bc.chain[0].index))
print("transactions = {}".format(probe_bc.chain[0].transactions))
print("timestamp = {}".format(probe_bc.chain[0].timestamp))
print("previous_hash = {}".format(probe_bc.chain[0].previous_hash))

probe_bc.chain[0]
print(probe_bc.chain[0])

print("hash = {}".format(probe_bc.chain[0].compute_hash()))