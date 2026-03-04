from flask import Flask, render_template, request, redirect
import os
import sys
import csv
from datetime import datetime
from collections import defaultdict

app = Flask(__name__, template_folder="templates", static_folder="static")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from leitor import carregar_perfil, carregar_transacoes
from calculadora import calcular_resumo

ARQUIVO_CSV = "../data/transacoes.csv"

def filtrar_por_mes(transacoes, mes):
    if not mes:
        return transacoes

    filtradas = []
    for t in transacoes:
        if t["data"].startswith(mes):
            filtradas.append(t)
    return filtradas


def calcular_evolucao_mensal(transacoes):
    meses = defaultdict(float)
    for t in transacoes:
        mes = t["data"][:7]
        if t["tipo"] == "saida":
            meses[mes] += t["valor"]
    return dict(meses)


@app.route("/", methods=["GET"])
def dashboard():
    perfil = carregar_perfil("../data/perfil_usuario.json")
    transacoes = carregar_transacoes(ARQUIVO_CSV)

    mes = request.args.get("mes")
    transacoes = filtrar_por_mes(transacoes, mes)

    total_receitas, total_despesas, saldo, despesas_categoria = calcular_resumo(transacoes)

    evolucao = calcular_evolucao_mensal(transacoes)

    percentual_gasto = 0
    if total_receitas > 0:
        percentual_gasto = (total_despesas / total_receitas) * 100

    return render_template(
        "dashboard.html",
        perfil=perfil,
        receitas=total_receitas,
        despesas=total_despesas,
        saldo=saldo,
        percentual=percentual_gasto,
        categorias=despesas_categoria,
        evolucao=evolucao,
        mes_selecionado=mes
    )


@app.route("/add", methods=["POST"])
def adicionar_transacao():
    data = request.form["data"]
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    valor = request.form["valor"]
    tipo = request.form["tipo"]

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data, descricao, categoria, valor, tipo])

    return redirect("/")

def responder_pergunta(pergunta, total_receitas, total_despesas, saldo, despesas_categoria, evolucao):
    pergunta = pergunta.lower()

    # 🔹 Está no vermelho?
    if "vermelho" in pergunta or "saldo" in pergunta:
        if saldo < 0:
            return f"Você está no vermelho. Seu saldo atual é de R$ {saldo:.2f}."
        else:
            return f"Seu saldo está positivo em R$ {saldo:.2f}. Boa gestão."

    # 🔹 Maior categoria de gasto
    if "maior gasto" in pergunta or "gasto maior" in pergunta:
        if despesas_categoria:
            maior_categoria = max(despesas_categoria, key=despesas_categoria.get)
            valor = despesas_categoria[maior_categoria]
            return f"Sua maior categoria de gasto é '{maior_categoria}' com R$ {valor:.2f}."
        else:
            return "Não encontrei despesas registradas."

    # 🔹 Mês com maior despesa
    if "mes" in pergunta and ("mais gastei" in pergunta or "maior" in pergunta):
        if evolucao:
            maior_mes = max(evolucao, key=evolucao.get)
            valor = evolucao[maior_mes]
            return f"O mês em que você mais gastou foi {maior_mes}, com R$ {valor:.2f}."
        else:
            return "Não há dados suficientes para analisar os meses."

    # 🔹 Pergunta por categoria dinâmica
    for categoria in despesas_categoria:
        if categoria.lower() in pergunta:
            valor = despesas_categoria[categoria]
            percentual = (valor / total_receitas) * 100 if total_receitas > 0 else 0
            return f"Você gastou R$ {valor:.2f} com {categoria}, equivalente a {percentual:.2f}% da sua renda."

    # 🔹 Economia
    if "economizar" in pergunta or "poupar" in pergunta:
        if total_receitas > 0:
            meta = total_receitas * 0.2
            return f"O ideal seria guardar pelo menos R$ {meta:.2f} (20% da sua renda)."
        else:
            return "Não há receitas registradas para calcular meta de economia."

    # 🔹 Análise automática
    if "analise" in pergunta or "resumo" in pergunta:
        if total_receitas > 0:
            percentual = (total_despesas / total_receitas) * 100
            return (
                f"Resumo do período:\n"
                f"Receitas: R$ {total_receitas:.2f}\n"
                f"Despesas: R$ {total_despesas:.2f}\n"
                f"Você comprometeu {percentual:.2f}% da sua renda."
            )
        else:
            return "Não há dados suficientes para análise."

    return "Ainda estou aprendendo. Tente perguntar sobre maior gasto, mês que mais gastou, saldo ou análise."


@app.route("/chat", methods=["GET", "POST"])
def chat():
    resposta = None
    pergunta = None

    if request.method == "POST":
        pergunta = request.form["pergunta"]

        transacoes = carregar_transacoes(ARQUIVO_CSV)
        total_receitas, total_despesas, saldo, despesas_categoria = calcular_resumo(transacoes)

        evolucao = calcular_evolucao_mensal(transacoes)

        resposta = responder_pergunta(
            pergunta,
            total_receitas,
            total_despesas,
            saldo,
            despesas_categoria,
            evolucao
        )

    return render_template(
        "chat.html",
        pergunta=pergunta,
        resposta=resposta
    )

if __name__ == "__main__":
    app.run(debug=True)
