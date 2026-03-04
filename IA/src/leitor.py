import json
import csv


def carregar_perfil(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_transacoes(caminho):
    transacoes = []
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["valor"] = float(row["valor"])
            transacoes.append(row)
    return transacoes