
from flask import Flask, request
import requests
import logging
import pandas as pd
import openpyxl

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"
ACCESS_TOKEN = "EAAPlmE1bNocBPRDc8dodJ1K5A37eyvGZCWVhuAS2GZAN1Cdjpp9fg2NRstIldfyKUsg3ZBe44I1C8sPRlJYMcVF9zZBiOVnuJaDLtF8mDmpFLdsqEYBXCXZBCdzSZBIHzL6a6PLwTP2Fc0SaSWg1e3tjdmcMvoNkfIvj4KWvZB43vqxfpt0Jg2ocAHWsAnDBZC0ZBUjvKfpkYMDcPBqAV0QNMDhKURDIBQ5TuZAUOMeD2MswZDZD"
IG_USER_ID = "17841476681185971"  # Este es tu ID de Instagram Business

logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        logging.info("Webhook verificado correctamente")
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        logging.info(f"Evento recibido: {data}")

        entries = data.get("entry", [])
        for entry in entries:
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                sender_id = event.get("sender", {}).get("id")
                message_text = event.get("message", {}).get("text", "")

                if not sender_id or not message_text:
                    continue  # Saltamos si falta info

                # Obtenemos el username de Instagram
                try:
                    url = f"https://graph.facebook.com/v19.0/{sender_id}"
                    params = {"fields": "username", "access_token": ACCESS_TOKEN}
                    response = requests.get(url, params=params)
                    user_data = response.json()
                    username = user_data.get("username", sender_id)
                except Exception as e:
                    logging.error(f"No se pudo obtener el username: {e}")
                    username = sender_id

                logging.info(f"Mensaje recibido de {username}: {message_text}")

                # Comprobamos "rutina"
                if "rutina" in message_text.lower():
                    usuario = username
                    campaña = message_text
                    df = pd.DataFrame([[usuario, campaña]], columns=["usuario", "campaña"])

                    excel_file = os.path.join("/tmp", "campanyas.xlsx")
                    try:
                        existing_df = pd.read_excel(excel_file)
                        df = pd.concat([existing_df, df], ignore_index=True)
                    except FileNotFoundError:
                        pass

                    df.to_excel(excel_file, index=False)
                    logging.info(f"✅ Datos guardados en {excel_file}")
                else:
                    logging.info("❌ La cadena no contiene 'rutina'")

    except Exception as e:
        logging.error(f"Error en webhook: {e}")

    # Siempre devolver algo válido
    return "ok", 200

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    params = {"access_token": ACCESS_TOKEN}
    response = requests.post(url, json=payload, params=params, headers=headers)
    logging.info(f"Respuesta API Messenger: {response.status_code} {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
