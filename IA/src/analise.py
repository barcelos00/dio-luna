def gerar_relatorio(perfil, total_receitas, total_despesas, saldo, despesas_categoria):

    print("\n===== RELATÓRIO FINANCEIRO LUNA =====\n")

    print(f"Usuário: {perfil.get('nome')}")
    print(f"Profissão: {perfil.get('profissao')}")
    print(f"Objetivo: {perfil.get('objetivo_principal')}")

    print("\n--- Resumo Geral ---")
    print(f"Total de Receitas: R$ {total_receitas:.2f}")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print(f"Saldo Final: R$ {saldo:.2f}")

    if total_receitas > 0:
        percentual = (total_despesas / total_receitas) * 100
        print(f"Percentual da renda comprometida: {percentual:.2f}%")

    print("\n--- Despesas por Categoria ---")
    for categoria, valor in despesas_categoria.items():
        print(f"{categoria}: R$ {valor:.2f}")

    print("\n--- Análise Inteligente ---")

    # Regra dos 30% moradia
    if "moradia" in despesas_categoria:
        percentual_moradia = (despesas_categoria["moradia"] / total_receitas) * 100
        if percentual_moradia > 30:
            print("Atenção: Moradia acima de 30% da renda.")
        else:
            print("Moradia dentro do limite recomendado.")

    # Método 50-30-20
    necessidades = total_receitas * 0.5
    qualidade = total_receitas * 0.3
    poupanca = total_receitas * 0.2

    print("\nReferência 50-30-20:")
    print(f"50% Necessidades: R$ {necessidades:.2f}")
    print(f"30% Qualidade de vida: R$ {qualidade:.2f}")
    print(f"20% Metas/Poupança: R$ {poupanca:.2f}")

    if saldo > 0:
        print("\nSugestão: Direcione o saldo para sua reserva de emergência.")

    print("\n=====================================\n")