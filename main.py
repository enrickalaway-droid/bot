from flask import Flask, request
import requests
import logging

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAAPlmE1bNocBPRDc8dodJ1K5A37eyvGZCWVhuAS2GZAN1Cdjpp9fg2NRstIldfyKUsg3ZBe44I1C8sPRlJYMcVF9zZBiOVnuJaDLtF8mDmpFLdsqEYBXCXZBCdzSZBIHzL6a6PLwTP2Fc0SaSWg1e3tjdmcMvoNkfIvj4KWvZB43vqxfpt0Jg2ocAHWsAnDBZC0ZBUjvKfpkYMDcPBqAV0QNMDhKURDIBQ5TuZAUOMeD2MswZDZD"  # Pon aquí tu token válido de página vinculada Instagram
IG_USER_ID = "17841476681185971"  # Pon aquí el ID de tu cuenta Instagram Business

logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        logging.info("Verificación webhook exitosa")
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info(f"Evento recibido: {data}")

    # Procesar mensajes entrantes
    entry = data.get("entry", [])
    for e in entry:
        messaging = e.get("messaging", [])
        for message_event in messaging:
            sender_id = message_event["sender"]["id"]
            logging.info(f"Mensaje de {sender_id}: {message_event.get('message', {}).get('text')}")

            # Aquí enviamos la respuesta con botones (quick_replies)
            send_quick_replies(sender_id)

    return "ok", 200

def send_quick_replies(recipient_id):
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/messages"
    headers = {"Content-Type": "application/json"}

    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": "Hola, elige una opción:",
            "quick_replies": [
                {"content_type": "text", "title": "Infórmate", "payload": "INFO_PAYLOAD"},
                {"content_type": "text", "title": "Contactar con Emilio", "payload": "CONTACTAR_PAYLOAD"},
                {"content_type": "text", "title": "Planes adaptados", "payload": "PLANES_PAYLOAD"}
            ]
        }
    }

    params = {"access_token": ACCESS_TOKEN}
    response = requests.post(url, json=payload, params=params, headers=headers)
    logging.info(f"Respuesta de la API de Messenger: {response.status_code} {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

