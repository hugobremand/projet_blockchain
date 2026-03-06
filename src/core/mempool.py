class Mempool:
    def __init__(self):
        """
        Contient les transactions en attente.
        """
        self.transactions = []

    def add_transaction(self, transaction, public_key):
        """
        Ajoute une transaction si elle est valide.
        """
        if public_key is not None:
            if not transaction.is_valid(public_key):
                raise ValueError("Invalid transaction signature")

        self.transactions.append(transaction)

    def remove_transactions(self, transactions):
        """
        Supprime les transactions déjà incluses dans un bloc.
        """
        for tx in transactions:
            if tx in self.transactions:
                self.transactions.remove(tx)

    def get_all_transactions(self):
        return self.transactions