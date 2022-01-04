from hashlib import sha256
import json
# import time

class Block:
    """
    El término genérico «información» es generlamente reemplazado en internet por el término «transacción». 
    Por ende, para evitar confusiones y ser consistentes, estaremos empleando el término «transacción» para 
    referirnos a información publicada en nuestra aplicación de ejemplo.
    
    Las transacciones están empaquetadas en bloques. Además, un bloque puede contener una o más transacciones. 
    Los bloques que contienen las transacciones son generados frecuentemente y añadidos al blockchain. Dado que 
    puede haber múltiples bloques, cada uno tendría que tener un identificador único.

    Encadenar los bloques

    Necesitamos una solución para asegurarnos que cualquier cambio en los bloques anteriores invalide la cadena 
    entera. Una forma de hacer esto es encadenar los bloques por su hash. Al encadenarlos de esta forma, queremos 
    decir incluir el hash del bloque anterior en el actual. Así, si el contenido de cualquiera de los bloques 
    anteriores cambia, el hash del bloque va a cambiar, llevando a una discrepancia con el campo previos_hash en
    el próximo bloque.
    """
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index 
        self.transactions = transactions 
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        """
        A function that return the hash of the block contents.

        Hacer los bloques inmutables

        Nos gustaría detectar cualquier tipo de manipulación en la información almacenada dentro de un bloque. 
        En blockchain, esto se hace usando una función hash.
        
        Una función hash es una función que toma información de cualquier tamaño y a partir de ella produce otra
        información de un tamaño fijo, que generalmente sirve para identificar la entrada [input]. 
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def __str__(self):
        out_str = """
        Block:
            index: {index}
            transactions: {transactions}
            timestamp: {timestamp}
            previous_hash: {previous_hash}
        """.format(index = self.index, \
                   transactions = self.transactions, \
                   timestamp = self.timestamp, \
                   previous_hash = self.previous_hash)

        return(out_str)

    def __repr__(self):
        out_str = "Block({index}, {transactions}, {timestamp}, '{previous_hash}')" \
            .format(index = self.index, \
                   transactions = self.transactions, \
                   timestamp = self.timestamp, \
                   previous_hash = self.previous_hash)

        return(out_str)