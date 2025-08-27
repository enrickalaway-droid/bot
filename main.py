from flask import Flask, request
import logging

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_secreto_123"

logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        logging.info("Webhook verificado correctamente")
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info(f"Evento recibido: {data}")

    entries = data.get("entry", [])
    for entry in entries:
        messaging_events = entry.get("messaging", [])
        for event in messaging_events:
            sender_id = event.get("sender", {}).get("id")
            message_text = event.get("message", {}).get("text")
            if sender_id and message_text:
                logging.info(f"Mensaje recibido de {sender_id}: {message_text}")

    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


