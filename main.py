from flask import Flask, render_template, request, jsonify
from uuid import uuid4
from transactions import Blockchain
from subscription import SubscriptionManager

app = Flask(__name__)

blockchain = Blockchain()
subscription_manager = SubscriptionManager()

node_identifier = str(uuid4()).replace('-', '')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        sender = request.form.get('sender')
        recipient = request.form.get('recipient')
        amount = float(request.form.get('amount'))
        index = blockchain.new_transaction(sender, recipient, amount)
        return render_template('transaction_result.html', message=f'Transaction will be added to Block {index}')
    else:
        return render_template('transactions.html', transactions=blockchain.get_all_transactions())

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    block = blockchain.new_block(proof)

    return render_template('mine.html', block=block)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return render_template('chain.html', chain=response['chain'], length=response['length'])

@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        plan = request.form.get('plan')
        amount = float(request.form.get('amount'))
        interval_days = int(request.form.get('interval_days'))
        subscription = subscription_manager.add_subscription(user_id, plan, amount, interval_days)
        return render_template('subscription_result.html', subscription=subscription)
    else:
        return render_template('subscriptions.html', subscriptions=subscription_manager.get_subscriptions())

if __name__ == '__main__':
    app.run(port=5000, debug=True)