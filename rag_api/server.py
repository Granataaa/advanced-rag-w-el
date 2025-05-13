import connexion
from flask_cors import CORS
from rag_service import loading

# Crea l'app Connexion
app = connexion.App(__name__, specification_dir='./swagger')
app.add_api('openapi.yaml', swagger_ui=True)

CORS(app.app)

# Usa Connexion per avviare il server senza uvicorn
if __name__ == "__main__":
    loading()
    app.run(host="0.0.0.0", port=5000)