
import time

import app.block

class Blockchain:

    # difficulty of our PoW algorithm
    difficulty = 2
 
    def __init__(self):
        """
        Bien, hemos montado los bloques. El blockchain supuestamente tiene que ser una colección de bloques. 
        Podemos almacenar todos los bloques en una lista de Python (el equivalente a un arreglo [array]). 
        Pero esto no es suficiente, porque ¿qué sucedería si alguien intencionalmente reemplaza un bloque en la 
        colección? Crear un nuevo bloque con transacciones alteradas, calcular el hash, y reemplazarlo por 
        cualquier otro bloque anterior no es una gran tarea en nuestra implementación actual, porque 
        mantendremos la inmutabilidad y el orden de los bloques.
        
        Necesitamos una solución para asegurarnos que cualquier cambio en los bloques anteriores invalide la 
        cadena entera. Una forma de hacer esto es encadenar los bloques por su hash. Al encadenarlos de esta 
        forma, queremos decir incluir el hash del bloque anterior en el actual. Así, si el contenido de 
        cualquiera de los bloques anteriores cambia, el hash del bloque va a cambiar, llevando a una 
        discrepancia con el campo previos_hash en el próximo bloque.
        """
        self.unconfirmed_transactions = [] # información para insertar en el blockchain
        self.chain = []
        self.create_genesis_block()
 
    def create_genesis_block(self):
        """
        Una función para generar el bloque génesis y añadirlo a la
        cadena. El bloque tiene index 0, previous_hash 0 y un hash
        válido.

        Perfecto, cada bloque está enlazado al anterior por el campo previous_hash, ¿pero qué sucede con el primer 
        bloque de todos? El primer bloque es llamado el bloque génesis y es generado manualmente o por alguna lógica 
        única, en la mayoría de los casos.
        """
        genesis_block = app.block.Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
 
    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.

        Aunque hay un problema. Si cambiamos el bloque anterior, podemos recalcular los hashes de todos los bloques 
        subsiguientes sencillamente y crear un blockchain diferente pero válido. Para prevenir esto, tenemos que 
        hacer que la tarea de calcular un hash sea difícil y aleatoria.
        
        Así es como se hace. En lugar de aceptar cualquier hash para el bloque, le agregaremos alguna condición. 
        Agreguemos una condición que nuestro hash deba empezar con dos ceros. Además, sabemos que a menos que 
        cambiemos el contenido del bloque, el hash no va a cambiar.
        
        Por lo que vamos a introducir un nuevo campo en nuestro bloque llamado nonce. Un nonce es un número que 
        cambiará constantemente hasta que obtengamos un hash que satisfaga nuestra condición. El número de ceros 
        prefijados (el valor 2, en nuestro caso) decide la «dificultad» de nuestro algoritmo de prueba de trabajo. 
        Además, notarás que nuestra prueba de trabajo es difícil de calcular pero fácil de verificar una vez que 
        averiguamos el nonce (para verificar, simplemente tienes que ejecutar la función hash nuevamente).
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.

         El proceso de poner transacciones no confirmadas en un bloque y calcular la prueba de trabajo es 
         conocido como el minado [mining] de bloques. Una vez que el nonce que satisface nuestra condición 
         es averiguado, podemos decir que el bloque ha sido minado, y es colocado en el blockchain.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = app.block.Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        return True
