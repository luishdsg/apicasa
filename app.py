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

collection = db.check

def serialize_item(item):
    item['_id'] = str(item['_id'])  # Converte ObjectId para string
    return item

@app.route('/item', methods=['GET', 'PATCH'])
def manage_item():
    if request.method == 'GET':
        items = list(collection.find())
        return jsonify([serialize_item(item) for item in items]), 200

    if request.method == 'PATCH':
        data = request.json
        
        # Verifica se o ID está presente
        item_id = data.get('_id')
        if not item_id:
            return jsonify({"error": "ID is required"}), 400
        
        # Converte o ID para ObjectId
        try:
            object_id = ObjectId(item_id)
        except Exception:
            return jsonify({"error": "Invalid ObjectId format"}), 400
        
        # Prepara os dados para atualização
        updates = {
            "valor": data.get('valor'),
            "name": data.get('name')
        }

        # Atualiza o item no banco de dados
        result = collection.update_one(
            {"_id": object_id},
            {"$set": updates}
        )

        if result.modified_count > 0:
            return jsonify({"message": "Item updated successfully"}), 200
        return jsonify({"error": "No changes made or item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
