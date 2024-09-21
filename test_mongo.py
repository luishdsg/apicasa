from pymongo import MongoClient

uri = "mongodb+srv://adm:qyVIEuWrZ89GhpAV@adm.6jacvht.mongodb.net/test"

client = MongoClient(uri)

try:
    client.admin.command('ping')  # Testa a conexão
    print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro ao conectar:", e)
finally:
    client.close()
