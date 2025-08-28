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

                    excel_file = "campanyas.xlsx"
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
