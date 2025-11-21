from flask import Flask, request
import datetime

app = Flask(__name__)

ATIVACOES_LOG = "ativacoes.txt"

@app.route("/ativar")
def ativar():
    codigo = request.args.get("codigo", "").strip()
    ip = request.remote_addr
    so = request.headers.get("User-Agent", "desconhecido")
    momento = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if not codigo:
        return "Código não enviado", 400

    with open(ATIVACOES_LOG, "a", encoding="utf-8") as f:
        f.write(f"{momento} | Código: {codigo} | IP: {ip} | SO: {so}\n")

    return f"Código {codigo} registrado com sucesso!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
