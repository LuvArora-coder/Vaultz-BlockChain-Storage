from flask import Flask, render_template, jsonify, request, flash, redirect
from utils.blockchain import Blockchain
from utils.document import Document
import hashlib
import logging
import socket, errno

blockchain = Blockchain()
blockchain.start_mining()

app = Flask(__name__)
app.secret_key = 'super secret key'
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def index():
    return render_template('explore.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
        else:
            file = request.files['file']
            description = request.form.get('description')
            checksum = hashlib.sha256(file.read()).hexdigest()

            existing_block = blockchain.look_for_document_by_checksum(checksum)

            if existing_block:
                flash('This file already exists')
                return redirect('/block/' + str(existing_block['block'].hash))

            doc = Document(checksum, description)
            blockchain.append_document(doc)
            flash('Document with checksum ' + checksum + ' uploaded and enqueued in blockchain');

            return redirect('/')

    return render_template('upload.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')

        file = request.files['file']
        checksum = hashlib.sha256(file.read()).hexdigest()
        result = blockchain.look_for_document_by_checksum(checksum)
        return render_template('verify_result.html', result=result)

    return render_template('verify.html')

@app.route('/block/<hash>')
def view_block(hash):
    block = blockchain.get_block_by_hash(hash)
    return render_template('view_block.html', block=block)

@app.route('/api/dumpChain')
def dump_chain():
    return jsonify(blockchain.dump_chain())

def run_server():
    app.run(host='127.0.0.1', port=8000)

run_server()