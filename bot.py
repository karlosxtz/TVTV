import requests
import os
from flask import Flask, request

app = Flask(__name__)

# TOKEN DO SEU BOT
TELEGRAM_TOKEN = "8333600201:AAGXsPe3ilm8bwSwu8Rws5Lw6wtUZJ0mAD4"

# API IPTV
API_URL = "https://fireplay.paneltop.online/api/chatbot/OALyoolW4w/ryJDzKWgeV"

# URL base do Telegram
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


# ============================
# FUNÇÃO PARA ENVIAR MENSAGEM
# ============================
def enviar_mensagem(chat_id, texto):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


# ============================
# ROTA PRINCIPAL (Render testa aqui)
# ============================
@app.route("/", methods=["GET"])
def home():
    return "Bot ativo! 🔥", 200


# ============================
# WEBHOOK
# ============================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return "no update"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        texto = update["message"].get("text", "")

        if texto == "/start":
            enviar_mensagem(
                chat_id,
                "🔥 *Bem-vindo ao StreamKeyBR!*\nUse /teste para gerar seu teste IPTV automático."
            )

        elif texto == "/teste":
            try:
                resposta = requests.get(API_URL)

                # Caso a API retorne página HTML da Cloudflare
                if "<html>" in resposta.text.lower():
                    enviar_mensagem(
                        chat_id, 
                        "❌ O servidor da API retornou erro (Cloudflare / HTML). Tente novamente mais tarde."
                    )
                    return "ok"

                dados = resposta.text.strip()
                enviar_mensagem(chat_id, f"🔥 *Seu teste está pronto!*\n\n{dados}")

            except Exception as e:
                enviar_mensagem(chat_id, "❌ Erro ao gerar o teste. Tente novamente.")
                print("Erro API:", e)

    return "ok"


# ============================
# INICIAR SERVIDOR (Render)
# ============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
