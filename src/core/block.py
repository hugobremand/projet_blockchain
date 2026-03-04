import hashlib
import json
import time


class BlockHeader:
    def __init__(self, previous_hash):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.merkle_root = None

    def to_dict(self):
        return {
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }


class Block:
    def __init__(self, previous_hash, transactions):
        self.transactions = transactions
        self.header = BlockHeader(previous_hash)

        self.header.merkle_root = self.compute_merkle_root()

        self.hash = self.compute_hash()

    def compute_merkle_root(self):
        if not self.transactions:
            return hashlib.sha256("".encode()).hexdigest()

        tx_hashes = [tx.compute_hash() for tx in self.transactions]

        combined = "".join(tx_hashes)

        return hashlib.sha256(combined.encode()).hexdigest()

    def compute_hash(self):
        block_string = json.dumps(self.header.to_dict(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine(self, difficulty):
        """
        Proof of Work :
        Le hash du bloc doit commencer par 'difficulty' zéros.
        """
        prefix = "0" * difficulty

        while True:
            self.hash = self.compute_hash()

            if self.hash.startswith(prefix):
                break

            self.header.nonce += 1