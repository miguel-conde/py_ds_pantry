import sys

sys.path.append("..")

import app

probe = app.block.Block(index = 0, 
                        transactions = [1, 2, 3], 
                        timestamp = "ts", 
                        previous_hash="kk")

print("index = {}".format(probe.index))
print("transactions = {}".format(probe.transactions))
print("timestamp = {}".format(probe.timestamp))
print("previous_hash = {}".format(probe.previous_hash))

probe
print(probe)

print("hash = {}".format(probe.compute_hash()))