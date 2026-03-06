# Mini Blockchain en Python

## Présentation

Ce projet est une **implémentation simplifiée d'une blockchain** réalisée en Python dans un objectif pédagogique.
Il permet de comprendre les concepts fondamentaux des blockchains modernes comme Bitcoin ou Ethereum.

Le projet implémente :

* une **blockchain**
* des **transactions**
* une **mempool**
* un système de **minage (Proof of Work)**
* un **calcul de balance**
* une **API REST avec Flask**
* une **interface web simple pour interagir avec la blockchain**

Cette blockchain est volontairement simplifiée pour faciliter la compréhension.

---

# Architecture du projet

```
projet_blockchain
│
├── src
│   ├── api
│   │   └── app.py              # API Flask
│   │
│   ├── core
│   │   ├── block.py            # Structure d'un bloc
│   │   ├── chain.py            # Gestion de la blockchain
│   │   ├── transaction.py      # Modèle de transaction
│   │   └── mempool.py          # Pool de transactions en attente
│   │
│   ├── crypto
│   │   ├── keys.py             # Génération de clés
│   │   └── signature.py        # Signature et vérification
│
├── templates
│   └── index.html              # Interface web
│
├── tests                       # Tests unitaires
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Fonctionnalités implémentées

## Blockchain

La blockchain est composée d'une **liste de blocs**.
Chaque bloc contient :

* le **hash du bloc précédent**
* une **liste de transactions**
* un **nonce**
* un **hash du bloc**

Le lien entre les blocs garantit l'intégrité de la chaîne.

---

## Transactions

Une transaction contient :

* un **expéditeur**
* un **destinataire**
* un **montant**
* un **nonce**
* une **signature**

Exemple :

```
Alice → Bob : 50
```

Les transactions sont d'abord placées dans la **mempool**.

---

## Mempool

La mempool est une **liste de transactions en attente** de validation.

Processus :

```
Transaction créée
↓
Ajout dans la mempool
↓
Minage d'un bloc
↓
Transaction ajoutée à la blockchain
```

---

## Minage (Proof of Work)

Le minage consiste à trouver un **nonce** tel que le hash du bloc respecte une difficulté donnée.

Exemple :

```
000ab234f5d9...
```

La difficulté actuelle est :

```
difficulty = 3
```

Le minage permet :

* de sécuriser la blockchain
* d'ajouter de nouveaux blocs

---

## Calcul des balances

Le solde d'une adresse est calculé en parcourant toute la blockchain.

```
balance = entrées - sorties
```

Exemple :

```
Alice reçoit 100
Alice envoie 30
Balance = 70
```

---

# API REST

L'API est développée avec **Flask**.

## Lancer l'API

```
python -m src.api.app
```

Le serveur démarre sur :

```
http://127.0.0.1:5000
```

---

# Endpoints disponibles

## Voir la blockchain

```
GET /chain
```

Retourne tous les blocs.

---

## Voir la mempool

```
GET /mempool
```

Retourne les transactions en attente.

---

## Envoyer une transaction

```
POST /transaction
```

Body JSON :

```
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 10
}
```

---

## Miner un bloc

```
POST /mine
```

Crée un bloc avec les transactions de la mempool.

---

## Balance d'une adresse

```
GET /balance/<address>
```

Exemple :

```
/balance/Alice
```

---

## Faucet (créer des coins)

```
POST /faucet/<address>
```

Permet de créer des coins pour tester la blockchain.

Exemple :

```
POST /faucet/Alice
```

Résultat :

```
SYSTEM → Alice : 100
```

---

# Interface Web

Une interface simple permet de :

* voir la blockchain
* voir la mempool
* envoyer des transactions
* miner un bloc
* utiliser un faucet

Accessible via :

```
http://127.0.0.1:5000
```

---

# Exemple d'utilisation

1️⃣ Créer des coins

```
Faucet Alice
```

2️⃣ Miner un bloc

```
Mine block
```

3️⃣ Envoyer une transaction

```
Alice → Bob : 40
```

4️⃣ Miner un bloc

La transaction apparaît dans la blockchain.

---

# Tests

Les tests sont réalisés avec **pytest**.

Lancer tous les tests :

```
pytest
```

---

# Installation

Cloner le projet :

```
git clone <repo>
cd projet_blockchain
```

Créer un environnement virtuel :

```
python -m venv venv
```

Activer l'environnement :

Windows :

```
venv\Scripts\activate
```

Installer les dépendances :

```
pip install -r requirements.txt
```

---

# Objectif pédagogique

Ce projet permet de comprendre :

* le fonctionnement d'une blockchain
* le rôle du hash
* les transactions
* le minage
* les signatures
* les mempools
* les API blockchain

---

# Améliorations possibles

* réseau P2P entre plusieurs nœuds
* gestion complète des signatures
* création de wallets
* interface plus avancée
* explorer blockchain complet
* smart contracts simplifiés

---

# Auteur

Projet réalisé dans le cadre d'un apprentissage des concepts de blockchain et des architectures distribuées.
