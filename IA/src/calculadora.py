from collections import defaultdict


def calcular_resumo(transacoes):
    total_receitas = 0
    total_despesas = 0
    despesas_por_categoria = defaultdict(float)

    for t in transacoes:
        if t["tipo"] == "entrada":
            total_receitas += t["valor"]
        elif t["tipo"] == "saida":
            total_despesas += t["valor"]
            despesas_por_categoria[t["categoria"]] += t["valor"]

    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo, despesas_por_categoria