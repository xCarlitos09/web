from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Configuración de rutas locales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'img')
DB_PRODUCTS = os.path.join(BASE_DIR, 'productos.json')
DB_CONFIG = os.path.join(BASE_DIR, 'config.json')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Inicialización de Bases de Datos
def init_json(path, data):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

init_json(DB_PRODUCTS, [])
init_json(DB_CONFIG, {"categories": ["Franelas", "Blusas", "Pijamas", "Almohadas"]})

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# --- API CATEGORÍAS ---
@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'GET':
        with open(DB_CONFIG, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    else:
        with open(DB_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(request.json, f, indent=4)
        return jsonify({"status": "ok"})

# --- API PRODUCTOS ---
@app.route('/api/products', methods=['GET'])
def get_products():
    with open(DB_PRODUCTS, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/upload', methods=['POST'])
def upload():
    files = request.files.getlist('photos')
    filenames = [f"img/{f.filename}" for f in files if f]
    for f in files:
        if f: f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    
    data = json.loads(request.form.get('data'))
    data['images'] = filenames
    
    with open(DB_PRODUCTS, 'r+', encoding='utf-8') as f:
        prods = json.load(f)
        prods.append(data)
        f.seek(0); json.dump(prods, f, indent=4); f.truncate()
    return jsonify({"status": "success"})

@app.route('/api/reorder', methods=['POST'])
def reorder():
    data = request.json
    with open(DB_PRODUCTS, 'r+', encoding='utf-8') as f:
        prods = json.load(f)
        for p in prods:
            if p['id'] == data['id']: p['images'] = data['images']
        f.seek(0); json.dump(prods, f, indent=4); f.truncate()
    return jsonify({"status": "reordered"})

@app.route('/api/toggle', methods=['POST'])
def toggle():
    id_p = request.json.get('id')
    with open(DB_PRODUCTS, 'r+', encoding='utf-8') as f:
        prods = json.load(f)
        for p in prods:
            if p['id'] == id_p: p['status'] = 'pausa' if p['status'] == 'activo' else 'activo'
        f.seek(0); json.dump(prods, f, indent=4); f.truncate()
    return jsonify({"status": "toggled"})

@app.route('/api/delete', methods=['POST'])
def delete():
    id_p = request.json.get('id')
    with open(DB_PRODUCTS, 'r+', encoding='utf-8') as f:
        prods = json.load(f)
        prods = [p for p in prods if p['id'] != id_p]
        f.seek(0); json.dump(prods, f, indent=4); f.truncate()
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)