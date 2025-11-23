import requests
import os
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = "https://fireplay.paneltop.online/api/chatbot/OALyoolW4w/ryJDzKWgeV"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def enviar_mensagem(chat_id, texto):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return "no update"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        texto = update["message"].get("text", "")

        if texto == "/start":
            enviar_mensagem(chat_id, "🔥 *Bem-vindo ao StreamKeyBR!* \nUse /teste para gerar seu teste IPTV automático.")

        elif texto == "/teste":
            try:
                resposta = requests.get(API_URL)
                dados = resposta.text  
                enviar_mensagem(chat_id, f"🔥 *Seu teste está pronto!*\n\n{dados}")
            except:
                enviar_mensagem(chat_id, "❌ Erro ao gerar o teste. Tente novamente.")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
