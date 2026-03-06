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

@app.route("/wallet/create", methods=["POST"])
def create_wallet():

    wallet = WalletKeys()

    # Convertir la clé privée en texte PEM
    private_key_bytes = wallet.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convertir la clé publique en texte PEM
    public_key_bytes = wallet.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convertir les bytes en string
    private_key = private_key_bytes.decode()
    public_key = public_key_bytes.decode()

    return jsonify({
        "public_key": public_key,
        "private_key": private_key
    }), 200

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):

    balance = blockchain.get_balance(address)

    return jsonify({
        "address": address,
        "balance": balance
    })

@app.route("/faucet/<address>", methods=["POST"])
def faucet(address):

    tx = Transaction(
        sender="SYSTEM",
        receiver=address,
        amount=100,
        nonce=0
    )

    tx.signature = "system"

    mempool.add_transaction(tx, None)

    return jsonify({
        "message": f"100 coins sent to {address}"
    }), 200


@app.route("/mempool", methods=["GET"])
def get_mempool():

    return jsonify([
        {
            "sender": tx.sender,
            "receiver": tx.receiver,
            "amount": tx.amount
        }
        for tx in mempool.transactions
    ])


@app.route("/transaction", methods=["POST"])
def add_transaction():

    data = request.get_json()

    required_fields = [
        "sender",
        "receiver",
        "amount"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    tx = Transaction(
        sender=data["sender"],
        receiver=data["receiver"],
        amount=int(data["amount"]),
        nonce=1
    )

    tx.signature = "demo"

    mempool.add_transaction(tx, None)

    return jsonify({
        "message": "Transaction added to mempool"
    }), 201


@app.route("/mine", methods=["POST"])
def mine():
    try:
        blockchain.mine_pending_transactions(mempool)
        return jsonify({"message": "Block mined successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)