from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define base directory
BASE_DIR = "/app/data"

# List files
@app.route('/list/<path:subpath>', methods=['GET'])
def list_files(subpath):
    abs_path = os.path.join(BASE_DIR, subpath)
    if os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        return jsonify(files)
    return jsonify({"error": "Path not found"}), 404

# Upload file
@app.route('/upload/<path:subpath>', methods=['POST'])
def upload_file(subpath):
    abs_path = os.path.join(BASE_DIR, subpath)
    if not os.path.exists(abs_path):
        return jsonify({"error": "Upload path does not exist"}), 400
    
    file = request.files['file']
    if file:
        file.save(os.path.join(abs_path, file.filename))
        return jsonify({"message": "File uploaded successfully"})
    return jsonify({"error": "No file uploaded"}), 400

# Parse scripts
@app.route('/parse/<path:filepath>', methods=['GET'])
def parse_scripts(filepath):
    abs_path = os.path.join(BASE_DIR, filepath)
    print(abs_path)
    if os.path.isfile(abs_path):
        # 找出 script 中設定的變數（以 $n 結尾的行）
        variables_lines = []
        try:
            with open(abs_path, 'r') as file:
                content = file.readlines()
            for line in content:
                if line.strip().endswith(tuple(f'${i}' for i in range(100))):
                    variables_lines.append(line.strip())
            return jsonify({"message": variables_lines})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found"}), 404

# Debug
@app.route('/debugA', methods=['GET'])
def debug():
    return jsonify({"message": "Debugging:A"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5987, debug=True)