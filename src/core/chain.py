from src.core.block import Block


class Blockchain:
    def __init__(self):
        self.chain = []
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
        if block.header.previous_hash != self.get_latest_block().compute_hash():
            raise ValueError("Previous hash incorrect")

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