from flask import Flask, request, send_file, jsonify
from cryptography.fernet import Fernet
import os
import uuid

app = Flask(__name__)

# Load encryption key
key_file = "secret.key"
if os.path.exists(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)
else:
    cipher = None

# Dictionary to store shared files and their passwords
shared_files = {}

@app.route('/share', methods=['POST'])
def share_file():
    data = request.form
    file_path = data.get('file_path')
    filename = data.get('filename')
    password = data.get('password')

    if not file_path or not filename or not password:
        return jsonify({"error": "Missing data"}), 400

    # Generate a unique file ID
    file_id = str(uuid.uuid4())
    shared_files[file_id] = {
        "file_path": file_path,
        "filename": filename,
        "password": password
    }
    return jsonify({"link": f"http://127.0.0.1:5000/share/{file_id}"}), 200

@app.route('/share/<file_id>', methods=['GET', 'POST'])
def download_file(file_id):
    if file_id not in shared_files:
        return jsonify({"error": "File not found"}), 404

    if request.method == 'POST':
        # Verify password
        password = request.form.get("password")
        if password == shared_files[file_id]["password"]:
            file_path = shared_files[file_id]["file_path"]
            return send_file(file_path, download_name=shared_files[file_id]["filename"], as_attachment=True)
        else:
            return jsonify({"error": "Invalid password"}), 401
    
    # Render password form
    return '''
        <h2>Enter password to download the file:</h2>
        <form method="post">
            Password: <input type="password" name="password">
            <input type="submit" value="Download">
        </form>
    '''

if __name__ == "__main__":
    app.run(port=5000)
