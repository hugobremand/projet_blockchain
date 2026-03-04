from src.core.block import Block


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 3
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            previous_hash="0",
            transactions=[]
        )
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        """
        Ajoute un bloc s'il est valide :
        - lien correct
        - preuve de travail valide
        - transactions valides
        """

        # Vérifie le lien
        if block.header.previous_hash != self.get_latest_block().hash:
            raise ValueError("Previous hash incorrect")

        # Vérifie la preuve de travail
        if not block.hash.startswith("0" * self.difficulty):
            raise ValueError("Invalid Proof of Work")

        # Vérifie les transactions
        for tx in block.transactions:
            if tx.signature is None:
                raise ValueError("Unsigned transaction in block")

        # Vérifie que le hash correspond bien au contenu
        if block.hash != block.compute_hash():
            raise ValueError("Block hash mismatch")

        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.header.previous_hash != previous_block.hash:
                return False

            if current_block.hash != current_block.compute_hash():
                return False

        return True
    
    def mine_pending_transactions(self, mempool):
        """
        Crée un bloc avec les transactions de la mempool,
        puis le mine.
        """
        if not mempool.transactions:
            raise ValueError("No transactions to mine")

        new_block = Block(
            previous_hash=self.get_latest_block().hash,
            transactions=mempool.get_all_transactions()
        )

        new_block.mine(self.difficulty)

        self.add_block(new_block)

        mempool.remove_transactions(new_block.transactions)