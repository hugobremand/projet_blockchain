import os
from flask import Flask, render_template, request, jsonify
from src.core.chain import Blockchain
from src.core.mempool import Mempool
from src.core.transaction import Transaction
from src.crypto.keys import WalletKeys
from src.crypto.signature import verify_signature
from cryptography.hazmat.primitives import serialization
import base64

template_dir = os.path.abspath("templates")

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    return render_template("index.html")

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

    return [
        {
            "sender": tx.sender,
            "receiver": tx.receiver,
            "amount": tx.amount
        }
        for tx in mempool.transactions
    ]


@app.route("/transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()

    required_fields = [
        "sender",
        "receiver",
        "amount",
        "signature",
        "public_key"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    # Reconstruction transaction
    tx = Transaction(
        sender=data["sender"],
        receiver=data["receiver"],
        amount=data["amount"],
        nonce=1
    )

    # Charger la clé publique envoyée (format PEM base64)
    public_key_bytes = base64.b64decode(data["public_key"])
    public_key = serialization.load_pem_public_key(public_key_bytes)

    # Décoder signature
    signature_bytes = base64.b64decode(data["signature"])

    # Vérifier signature
    if not verify_signature(
        public_key,
        tx.compute_hash().encode(),
        signature_bytes
    ):
        return jsonify({"error": "Invalid signature"}), 400

    tx.signature = signature_bytes

    mempool.add_transaction(tx, public_key)

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