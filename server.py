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
    token = "8500460958:AAGdLhco3b2K3Pl0Ia8cdw1FdMWXgt5H9fc"   # coloque o token do seu bot aqui

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
    nome = request.args.get("nome", "Desconhecido").strip()

    ip = request.remote_addr
    so = request.headers.get("User-Agent", "desconhecido")
    momento = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if not codigo:
        return "Código não enviado", 400

    # -------------------------------
    # VERIFICAR SE O CÓDIGO JÁ FOI USADO
    # -------------------------------
    codigo_ja_usado = False
    if os.path.exists(ATIVACOES_LOG):
        with open(ATIVACOES_LOG, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if f"Código: {codigo}" in conteudo or f"Codigo: {codigo}" in conteudo:
                codigo_ja_usado = True

    # -------------------------------
    # REGISTRAR USO NO ARQUIVO
    # -------------------------------
    with open(ATIVACOES_LOG, "a", encoding="utf-8") as f:
        f.write(f"{momento} | Nome: {nome} | Código: {codigo} | IP: {ip} | SO: {so}\n")

    # -------------------------------
    # MONTAR MENSAGEM COMPLETA
    # -------------------------------
    mensagem_detalhada = (
        f"{'⚠ ALERTA – O código ' + codigo + ' foi usado novamente por ' + nome + '!' if codigo_ja_usado else 'Novo código ativado por ' + nome + ': ' + codigo}\n"
        f"-------------------------------------------------------\n"
        f"📌 Detalhes:\n"
        f"• Nome: {nome}\n"
        f"• Código: {codigo}\n"
        f"• IP: {ip}\n"
        f"• SO: {so}\n"
        f"• Data/Hora: {momento}"
    )

    # -------------------------------
    # ENVIAR MENSAGEM
    # -------------------------------
    enviar_telegram(mensagem_detalhada)

    return f"Código {codigo} registrado com sucesso!"


# ==========================================================
#                   EXECUÇÃO LOCAL
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
