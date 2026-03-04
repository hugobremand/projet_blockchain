from flask import Flask, request, jsonify
from src.core.chain import Blockchain
from src.core.mempool import Mempool
from src.core.transaction import Transaction
from src.crypto.keys import WalletKeys

app = Flask(__name__)

blockchain = Blockchain()
mempool = Mempool()


@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = []

    for block in blockchain.chain:
        chain_data.append({
            "hash": block.hash,
            "previous_hash": block.header.previous_hash,
            "transactions": [
                {
                    "sender": tx.sender,
                    "receiver": tx.receiver,
                    "amount": tx.amount
                }
                for tx in block.transactions
            ]
        })

    return jsonify(chain_data), 200


@app.route("/mempool", methods=["GET"])
def get_mempool():
    return jsonify([
        {
            "sender": tx.sender,
            "receiver": tx.receiver,
            "amount": tx.amount
        }
        for tx in mempool.transactions
    ]), 200


@app.route("/transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()

    required_fields = ["sender", "receiver", "amount"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    tx = Transaction(
        sender=data["sender"],
        receiver=data["receiver"],
        amount=data["amount"],
        nonce=1
    )

    # Ici on ne gère pas encore la signature externe (simplification)
    tx.signature = "manual"

    mempool.transactions.append(tx)

    return jsonify({"message": "Transaction added to mempool"}), 201


@app.route("/mine", methods=["POST"])
def mine():
    try:
        blockchain.mine_pending_transactions(mempool)
        return jsonify({"message": "Block mined successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)