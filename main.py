from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAALQ3PHqEbsBPZAJOksv9a7BpFEeYyhZB7lHa0XCvS6x2RYoSqW5iJQKHLLwQRZBq2gSuS9ZAnfwyKfKa7YydR5ROlc3pmS2b4ZAZCo3l4TV8J6JZCFuRVAHHuSPp0DCoBuIr4NS4kQtUoX6UdwHxKAVkDCNMQcaZAnWOrZCcASLzWb728v9N5205AlZCly77twqrV4rCuSZCD6U9uryktMWzUFzgyHkfhZAyoVbwlySQ4JFXwZDZD"  # <-- Pega aquí tu token de acceso de página

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Evento recibido:", data)

    # Aquí puedes manejar los mensajes entrantes y responder
    return "ok", 200

@app.route('/')
def home():
    return "Servidor activo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
