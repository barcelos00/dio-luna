# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente "Edu" usando os 4 arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>
> [cole ou anexe o template `02-base-conhecimento.md` pra contexto]

## Dados Utilizados
| Arquivo                    | Formato | Para que serve na Luna?                                                                                  |
| -------------------------- | ------- | -------------------------------------------------------------------------------------------------------- |
| `perfil_usuario.json`      | JSON    | Identificar renda mensal, objetivos financeiros e preferências do usuário para personalizar o orçamento. |
| `gastos_mensais.csv`       | CSV     | Registrar e classificar despesas por categoria (fixas, variáveis, lazer, essenciais).                    |
| `metas_financeiras.json`   | JSON    | Acompanhar metas como reserva de emergência, viagens ou compra de bens.                                  |
| `historico_interacoes.csv` | CSV     | Manter continuidade no atendimento e acompanhar evolução dos hábitos financeiros.                        |

---

## Adaptações nos Dados

> Os dados mockados foram organizados para focar exclusivamente em educação financeira e organização de orçamento, removendo qualquer informação relacionada a:
> - Score de crédito
> - Produtos financeiros complexos
> - Recomendação de investimento específico
> - Dados bancários reais

Além disso:
>- As categorias de gastos foram padronizadas em:
>- Moradia
>- Alimentação
>- Transporte
>- Saúde
>- Lazer
>- Assinaturas
>- Outros

As metas financeiras foram estruturadas com:
>- Valor necessário
>- Valor atual
>- Prazo estimado

Isso permite que a Luna trabalhe de forma clara, educativa e alinhada às suas limitações.

---

## Estratégia de Integração

### Como os dados são carregados?
> Os arquivos podem ser carregados via código em python:


```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_usuario.json'))
gastos = pd.read_csv('./data/gastos_mensais.csv')
metas = json.load(open('./data/metas_financeiras.json'))
historico = pd.read_csv('./data/historico_interacoes.csv'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

A Luna recebe os dados estruturados dentro do contexto antes de gerar a resposta.
Eles podem ser inseridos no system prompt ou concatenados dinamicamente antes da pergunta do usuário.
Exemplo de injeção de contexto:

```text
DADOS DO USUÁRIO (perfil_usuario.json):
{
  "nome": "Mariana Costa",
  "idade": 27,
  "renda_mensal": 4200.00,
  "objetivo_principal": "Organizar orçamento e criar reserva de emergência",
  "preferencia_orcamento": "50-30-20"
}

GASTOS DO MÊS (gastos_mensais.csv):
data,descricao,categoria,valor
2026-02-01,Aluguel,Moradia,1300.00
2026-02-03,Supermercado,Alimentação,520.00
2026-02-05,Academia,Saúde,120.00
2026-02-07,Netflix,Assinaturas,55.90
2026-02-10,Uber,Transporte,180.00
2026-02-15,Restaurante,Lazer,240.00
2026-02-20,Conta de Luz,Moradia,190.00

METAS FINANCEIRAS (metas_financeiras.json):
[
  {
    "meta": "Reserva de emergência",
    "valor_necessario": 12000.00,
    "valor_atual": 4000.00,
    "prazo": "2026-12"
  }
]

HISTÓRICO DE INTERAÇÕES (historico_interacoes.csv):
data,tema,resumo
2026-01-10,Orçamento mensal,Usuária solicitou ajuda para classificar despesas
2026-01-25,Método 50-30-20,Explicação detalhada enviada
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.
Para otimizar tokens, os dados podem ser sintetizados antes de enviar ao modelo:

```DADOS DO USUÁRIO:
- Nome: Mariana Costa
- Renda mensal: R$ 4.200
- Objetivo principal: Criar reserva de emergência
- Método preferido: 50-30-20

RESUMO DE GASTOS:
- Moradia: R$ 1.490
- Alimentação: R$ 520
- Transporte: R$ 180
- Saúde: R$ 120
- Lazer: R$ 240
- Assinaturas: R$ 55,90
- Total de despesas: R$ 2.605,90

ANÁLISE AUTOMÁTICA:
- Percentual gasto: 62% da renda
- Potencial de economia: R$ 1.594,10
- Reserva atual: R$ 4.000
- Meta: R$ 12.000 até 12/2026

CONTEXTO DO ATENDIMENTO:
- Já recebeu explicação sobre método 50-30-20
- Já organizou despesas em fixas e variáveis anteriormente
```
