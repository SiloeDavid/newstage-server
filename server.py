from flask import Flask, request
import datetime
import requests
import os

app = Flask(__name__)

ATIVACOES_LOG = "ativacoes.txt"


# ==========================================================
#      FUNÇÃO PARA ENVIAR MENSAGEM NO TELEGRAM
# ==========================================================
def enviar_telegram(mensagem: str):
    token = "8500460958:AAGdLhco3b2K3Pl0Ia8cdw1FdMWXgt5H9fc"

    chat_ids = [
        "6503215200",   # você
        "6497450238"    # outra pessoa
    ]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for cid in chat_ids:
        data = {
            "chat_id": cid,
            "text": mensagem
        }

        try:
            requests.post(url, data=data, timeout=10)
            print(f"Mensagem enviada para {cid}")
        except Exception as e:
            print(f"Erro ao enviar mensagem para {cid}:", e)


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

    # -------------------------------
    # VERIFICAR SE JÁ FOI USADO
    # -------------------------------
    codigo_ja_usado = False
    if os.path.exists(ATIVACOES_LOG):
        with open(ATIVACOES_LOG, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if codigo in conteudo:
                codigo_ja_usado = True

    # -------------------------------
    # REGISTRAR ATIVAÇÃO
    # -------------------------------
    with open(ATIVACOES_LOG, "a", encoding="utf-8") as f:
        f.write(f"{momento} | Código: {codigo} | IP: {ip} | SO: {so}\n")

    # -------------------------------
    # ENVIAR MENSAGEM PARA TELEGRAM
    # -------------------------------
    if codigo_ja_usado:
        enviar_telegram(f"⚠ ALERTA: O código {codigo} foi usado novamente!")
    else:
        enviar_telegram(f"Novo código ativado: {codigo}")

    return f"Código {codigo} registrado com sucesso!"


# ==========================================================
#                   EXECUÇÃO LOCAL
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
