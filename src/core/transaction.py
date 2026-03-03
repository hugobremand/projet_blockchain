import json
import hashlib
from src.crypto.signature import sign_message, verify_signature


class Transaction:
    def __init__(self, sender, receiver, amount, nonce):
        """
        sender : adresse de l'émetteur
        receiver : adresse du destinataire
        amount : montant transféré
        nonce : numéro unique pour éviter le rejeu
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.nonce = nonce
        self.signature = None  # sera ajoutée après signature

    def to_dict(self):
        """
        Représentation dictionnaire (sans signature).
        Important pour le hash.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "nonce": self.nonce
        }

    def compute_hash(self):
        """
        Calcule le hash SHA-256 de la transaction.
        """
        tx_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign(self, private_key):
        """
        Signe la transaction avec la clé privée de l'émetteur.
        """
        message = self.compute_hash().encode()
        self.signature = sign_message(private_key, message)

    def is_valid(self, public_key):
        """
        Vérifie la validité de la transaction.
        """
        if self.signature is None:
            return False

        message = self.compute_hash().encode()
        return verify_signature(public_key, message, self.signature)