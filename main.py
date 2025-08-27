from flask import Flask, request
import logging
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAAPlmE1bNocBPRDc8dodJ1K5A37eyvGZCWVhuAS2GZAN1Cdjpp9fg2NRstIldfyKUsg3ZBe44I1C8sPRlJYMcVF9zZBiOVnuJaDLtF8mDmpFLdsqEYBXCXZBCdzSZBIHzL6a6PLwTP2Fc0SaSWg1e3tjdmcMvoNkfIvj4KWvZB43vqxfpt0Jg2ocAHWsAnDBZC0ZBUjvKfpkYMDcPBqAV0QNMDhKURDIBQ5TuZAUOMeD2MswZDZD"

logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    app.logger.info(f"Verify request - Mode: {mode}, Token: {token}, Challenge: {challenge}")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info(f"Evento recibido: {data}")

    if data and "entry" in data:
        for entry in data["entry"]:
            if "messaging" in entry:
                for event in entry["messaging"]:
                    if "message" in event:
                        sender_id = event["sender"]["id"]
                        message_text = event["message"].get("text", "")
                        app.logger.info(f"Mensaje de {sender_id}: {message_text}")

                        # Aquí puedes responder con botones
                        send_button_message(sender_id)

    return "ok", 200

def send_button_message(recipient_id):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}"

    message_data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "¿En qué te puedo ayudar?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Infórmate",
                            "payload": "INFO"
                        },
                        {
                            "type": "postback",
                            "title": "Contactar con Emilio",
                            "payload": "CONTACT"
                        },
                        {
                            "type": "postback",
                            "title": "Planes adaptados",
                            "payload": "PLANES"
                        }
                    ]
                }
            }
        }
    }

    response = requests.post(url, json=message_data)
    app.logger.info(f"Respuesta de la API de Messenger: {response.status_code} {response.text}")

@app.route('/')
def home():
    return "Servidor activo", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

