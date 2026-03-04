from leitor import carregar_perfil, carregar_transacoes
from calculadora import calcular_resumo
from analise import gerar_relatorio


def main():
    try:
        perfil = carregar_perfil("data/perfil_usuario.json")
        transacoes = carregar_transacoes("data/transacoes.csv")

        total_receitas, total_despesas, saldo, despesas_categoria = calcular_resumo(transacoes)

        gerar_relatorio(
            perfil,
            total_receitas,
            total_despesas,
            saldo,
            despesas_categoria
        )

    except FileNotFoundError:
        print("Erro: Arquivos não encontrados. Verifique a pasta data/.")

    except Exception as e:
        print("Erro inesperado:")
        print(e)


if __name__ == "__main__":
    main()