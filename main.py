from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAALQ3PHqEbsBPZAJOksv9a7BpFEeYyhZB7lHa0XCvS6x2RYoSqW5iJQKHLLwQRZBq2gSuS9ZAnfwyKfKa7YydR5ROlc3pmS2b4ZAZCo3l4TV8J6JZCFuRVAHHuSPp0DCoBuIr4NS4kQtUoX6UdwHxKAVkDCNMQcaZAnWOrZCcASLzWb728v9N5205AlZCly77twqrV4rCuSZCD6U9uryktMWzUFzgyHkfhZAyoVbwlySQ4JFXwZDZD"

def send_message_buttons(recipient_id):
    print(f"[send_message_buttons] Enviando botones a: {recipient_id}")
    url = 'https://graph.facebook.com/v18.0/me/messages'
    params = {'access_token': ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Elige una opción:",
                    "buttons": [
                        {"type": "postback", "title": "Infórmate", "payload": "INFO"},
                        {"type": "postback", "title": "Contactar con Emilio", "payload": "CONTACT_EMILIO"},
                        {"type": "postback", "title": "Planes adaptados", "payload": "PLANES"}
                    ]
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    response = requests.post(url, params=params, json=data)
    print("[send_message_buttons] Respuesta Facebook:", response.status_code, response.text)

def send_message_simple(recipient_id, text):
    print(f"[send_message_simple] Enviando mensaje simple a: {recipient_id}")
    url = 'https://graph.facebook.com/v18.0/me/messages'
    params = {'access_token': ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    response = requests.post(url, params=params, json=data)
    print("[send_message_simple] Respuesta Facebook:", response.status_code, response.text)

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    print(f"[verify] mode={mode}, token={token}, challenge={challenge}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[verify] Verificación exitosa")
        return challenge, 200
    print("[verify] Verificación fallida")
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("[webhook] Evento recibido:", data)

    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                print(f"[webhook] Evento de mensaje de sender_id: {sender_id}")
                if "message" in event:
                    send_message_buttons(sender_id)
                elif "postback" in event:
                    payload = event["postback"]["payload"]
                    print(f"[webhook] Postback recibido con payload: {payload}")
                    if payload == "INFO":
                        send_message_simple(sender_id, "Aquí tienes información importante...")
                    elif payload == "CONTACT_EMILIO":
                        send_message_simple(sender_id, "Puedes contactar a Emilio en: emilio@example.com")
                    elif payload == "PLANES":
                        send_message_simple(sender_id, "Estos son nuestros planes adaptados...")
    return "ok", 200

@app.route('/')
def home():
    return "Servidor activo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
