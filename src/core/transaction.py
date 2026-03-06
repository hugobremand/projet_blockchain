import json
import hashlib
from src.crypto.signature import sign_message, verify_signature


class Transaction:
    def __init__(self, sender, receiver, amount, nonce):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.nonce = nonce
        self.signature = None  

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "nonce": self.nonce
        }

    def compute_hash(self):
        tx_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign(self, private_key):
        message = self.compute_hash().encode()
        self.signature = sign_message(private_key, message)

    def is_valid(self, public_key):

        # Transaction système (mint)
        if self.sender == "SYSTEM":
            return True

        message = self.compute_hash().encode()
        return verify_signature(public_key, message, self.signature)