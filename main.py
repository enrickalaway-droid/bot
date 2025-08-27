from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAALQ3PHqEbsBPZAJOksv9a7BpFEeYyhZB7lHa0XCvS6x2RYoSqW5iJQKHLLwQRZBq2gSuS9ZAnfwyKfKa7YydR5ROlc3pmS2b4ZAZCo3l4TV8J6JZCFuRVAHHuSPp0DCoBuIr4NS4kQtUoX6UdwHxKAVkDCNMQcaZAnWOrZCcASLzWb728v9N5205AlZCly77twqrV4rCuSZCD6U9uryktMWzUFzgyHkfhZAyoVbwlySQ4JFXwZDZD"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

def send_message_buttons(recipient_id):
    url = 'https://graph.facebook.com/v18.0/me/messages'
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Selecciona una opción:",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Infórmate",
                            "payload": "INFO"
                        },
                        {
                            "type": "postback",
                            "title": "Contactar con Emilio",
                            "payload": "CONTACT_EMILIO"
                        },
                        {
                            "type": "postback",
                            "title": "Planes adaptados",
                            "payload": "PLANES"
                        }
                    ]
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    params = {"access_token": ACCESS_TOKEN}
    response = requests.post(url, headers=headers, params=params, json=data)
    print("Respuesta del envío:", response.json())

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Evento recibido:", data)

    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event:
                    send_message_buttons(sender_id)
    return "ok", 200

@app.route('/')
def home():
    return "Servidor activo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
