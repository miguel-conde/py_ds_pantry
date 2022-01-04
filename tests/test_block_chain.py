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


#### Añadir un bloque a la cadena
probe_block = app.block.Block(index = 1, 
                              transactions = [1, 2, 3], 
                              timestamp = "ts", 
                              previous_hash=probe_bc.last_block.hash)

proof_of_work = probe_bc.proof_of_work(probe_block)

probe_bc.is_valid_proof(probe_block, proof_of_work)

probe_block.hash = proof_of_work

probe_bc.chain.append(probe_block)

#### Añadir otro bloque a la cadena
probe_block = app.block.Block(index = 2, 
                              transactions = [1, 2, 3], 
                              timestamp = "ts", 
                              previous_hash=probe_bc.last_block.hash)

proof_of_work = probe_bc.proof_of_work(probe_block)
probe_bc.add_block(probe_block, proof_of_work)

##### MINADO

# El proceso de poner transacciones no confirmadas en un bloque y calcular la prueba de trabajo es 
# conocido como el minado [mining] de bloques. Una vez que el nonce que satisface nuestra condición 
# es averiguado, podemos decir que el bloque ha sido minado, y es colocado en el blockchain.

import time

new_transaction = [100, 101, 102]
probe_bc.unconfirmed_transactions.append(new_transaction)

if probe_bc.unconfirmed_transactions:
    
    last_block = probe_bc.last_block
 
    new_block = app.block.Block(index=last_block.index + 1,
                      transactions=probe_bc.unconfirmed_transactions,
                      timestamp=time.time(),
                      previous_hash=last_block.hash)

    proof = probe_bc.proof_of_work(new_block)
    probe_bc.add_block(new_block, proof)
    probe_bc.unconfirmed_transactions = []

# Otra, ahora con los métodos apropiado:
new_transaction = [200, 201, 202] # Nueva transacción
new_transaction2 = [300, 301, 302] # Nueva transacción

probe_bc.add_new_transaction(new_transaction) # Las añade a transtactions pendientes
probe_bc.add_new_transaction(new_transaction2)

# Con las transacciones pendienets genera un nuevo bloque y lo mina (busca un hash para él que
# satisfaga las condiciones de proof of work - cuando lo encuentra lo añade al final de la
# blockchain)
probe_bc.mine() # Minado de las transacciones pendientes