from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import hashlib
import os
from quantum import qkd, encrypt_message, decrypt_message

newSite = Flask(__name__)
newSite.secret_key = os.urandom(24)

def generate_new_key():
    shared_key = qkd()  # Quantum Key Distribution
    shared_key_hex = hashlib.sha256(str(shared_key).encode()).hexdigest()
    return shared_key, shared_key_hex

@newSite.route('/')
def index():
    return render_template("login.html")

# @newSite.route('/check', methods=['POST'])
# def check():
#     # check if current messages are up to date
#     # if not, update them
#     with open(str(session['key_hex']) + '.txt', 'a'):
#         lines = [line.rstrip('\n') for line in open(str(session['key_hex']) + '.txt')]
#         if len(lines) > 0:
#             last_line = lines[-1]
#             timestamp, timestamp2, user, nonce_hex, ciphertext_hex, tag_hex = last_line.split(" ")
#             nonce = bytes.fromhex(nonce_hex)
#             ciphertext = bytes.fromhex(ciphertext_hex)
#             tag = bytes.fromhex(tag_hex)
#             decrypted_message = decrypt_message(session['generated_key_hex'], nonce, ciphertext, tag)

@newSite.route('/request', methods=['POST'])
def request_key():
    shared_key, shared_key_hex = generate_new_key()
    # Save the generated key in the session
    session['generated_key_hex'] = shared_key_hex
    with open('circulatingkeys.txt', 'a') as keys_file:
        keys_file.write(shared_key_hex + "\n")
    # create a new file with the name of the key
    with open(str(shared_key_hex) + '.txt', 'a'):
        pass
    return shared_key_hex

@newSite.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('key_hex', None)
        username = request.form['uname']
        password = request.form['pass']

        # Check if the entered password matches any key in circulatingkeys.txt
        valid_key = False
        with open('circulatingkeys.txt', 'r') as keys_file:
            for line in keys_file:
                if line.strip() == password:
                    valid_key = True
                    break

        if username and username.strip() and valid_key:
            session['user'] = username
            session['key_hex'] = password  # Store the entered key hex in the session
            return redirect(url_for('chat'))
    return render_template('login.html')

@newSite.route('/chat', methods=['GET', 'POST'])
def chat():
    try:
        if 'user' not in session or 'key_hex' not in session:
            return redirect(url_for('login'))

        chat_file = session['key_hex'] + '.txt'
        shared_key = hashlib.sha256(session['key_hex'].encode()).digest()

        if request.method == 'POST':
            message = request.form.get('message', '')
            if message:
                nonce, ciphertext, tag = encrypt_message(shared_key, message)
                with open(chat_file, 'a') as chatFile:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    chatFile.write(f"{timestamp} {session['user']} {nonce.hex()} {ciphertext.hex()} {tag.hex()}\n")
                return redirect(url_for('chat'))

        if request.method == 'GET':
            chatHistory = []
            with open(chat_file, 'r') as chatFile:
                for line in chatFile:
                    line = line.strip()
                    if line:
                        # 2023-11-30 12:32:11 admin 3a6c83bfbfe4911db8966060819922da c04c4bdc3e 4040ade585d070cceb38fdb891a42a95
                        timestamp, timestamp2, user, nonce_hex, ciphertext_hex, tag_hex = line.split(" ")
                        nonce = bytes.fromhex(nonce_hex)
                        ciphertext = bytes.fromhex(ciphertext_hex)
                        tag = bytes.fromhex(tag_hex)
                        decrypted_message = decrypt_message(shared_key, nonce, ciphertext, tag)
                        chatHistory.append(f"{timestamp} {timestamp2} | {user}: {decrypted_message}")
                chatHistory.reverse()
            return render_template('chat.html', chatHistory=chatHistory)

    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('login'))

if __name__ == "__main__":
    newSite.run(debug=True)
