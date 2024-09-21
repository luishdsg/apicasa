from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
client = MongoClient(app.config['MONGO_URI'])
db = client.test  # Certifique-se de que o nome do banco está correto

# Acesse a subcoleção "check"
collection = db.check

# Função para converter o documento antes de retornar
def serialize_item(item):
    item['_id'] = str(item['_id'])  # Converte ObjectId para string
    return item

@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return jsonify(serialize_item(item)), 200
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/item/<item_id>', methods=['PATCH'])
def update_item(item_id):
    try:
        updates = request.json
        if not all(isinstance(v, bool) for v in updates.values()):
            return jsonify({"error": "All values must be boolean"}), 400

        result = collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": updates}
        )

        if result.modified_count > 0:
            return jsonify({"message": "Item updated successfully"}), 200
        return jsonify({"error": "No changes made or item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

