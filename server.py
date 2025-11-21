from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

ATIVACOES_LOG = "ativacoes.txt"


# ==========================================================
#      FUNÇÃO PARA ENVIAR MENSAGEM NO TELEGRAM
# ==========================================================
def enviar_telegram(mensagem: str):
    token = "8500460958:AAGdLhco3b2K3Pl0Ia8cdw1FdMWXgt5H9fc"
    chat_ids = [
    "6497450238",   
    "1763736530"   
]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": mensagem
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)


# ==========================================================
#                  ENDPOINT /ativar
# ==========================================================
@app.route("/ativar")
def ativar():
    codigo = request.args.get("codigo", "").strip()
    ip = request.remote_addr
    so = request.headers.get("User-Agent", "desconhecido")
    momento = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if not codigo:
        return "Código não enviado", 400

    # Registro em arquivo
    with open(ATIVACOES_LOG, "a", encoding="utf-8") as f:
        f.write(f"{momento} | Código: {codigo} | IP: {ip} | SO: {so}\n")

    # Enviar mensagem para o Telegram
    enviar_telegram(f"Novo código ativado: {codigo}")

    return f"Código {codigo} registrado com sucesso!"


# ==========================================================
#                   EXECUÇÃO LOCAL
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
