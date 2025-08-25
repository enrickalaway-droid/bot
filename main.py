from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "test-token"
ACCESS_TOKEN = "EAAB..."  # <-- Pega aquí tu token de acceso de página

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
