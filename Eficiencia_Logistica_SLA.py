import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuração estética padronizada para relatórios executivos
sns.set_theme(style="whitegrid")
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial"],
        "axes.edgecolor": "#cccccc",
        "axes.linewidth": 0.8,
    }
)

# -----------------------------------------------------------------------------
# 1. ENGENHARIA DE DADOS (Processamento do Dataset Olist)
# -----------------------------------------------------------------------------
"""
Exemplo de carregamento e merge das tabelas Olist:
orders = pd.read_csv('olist_orders_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')

df = orders.merge(customers, on='customer_id', how='inner')
df = df.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')

# Conversão para datetime
date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# Cálculo de colunas de SLA
df['tempo_entrega_dias'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
df['dias_atraso'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)
df['status_prazo'] = np.where(df['dias_atraso'] <= 0, 'No Prazo', 
                     np.where(df['dias_atraso'] <= 3, 'Atraso 1-3d', 'Atraso >7d'))
"""

# -----------------------------------------------------------------------------
# 2. GRÁFICO 1: TEMPO MÉDIO DE ENTREGA REAL POR ESTADO DESTINO
# -----------------------------------------------------------------------------
# Dados consolidados conforme apresentação
dados_estados = pd.DataFrame(
    {
        "Estado": ["São Paulo (SP)", "Rio de Janeiro (RJ)", "Bahia (BA)", "Ceará (CE)"],
        "Tempo_Medio_Dias": [8.3, 14.8, 18.5, 20.8],
        "Cor": ["#16a34a", "#0284c7", "#eab308", "#dc2626"],
    }
)

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(
    dados_estados["Estado"],
    dados_estados["Tempo_Medio_Dias"],
    color=dados_estados["Cor"],
    height=0.55,
)

# Rótulos de dados nas barras
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.4,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.1f} dias",
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="#1e293b",
    )

ax.set_title(
    "Tempo Médio de Entrega Real por Estado Destino (Dias)",
    fontsize=14,
    fontweight="bold",
    pad=20,
    color="#0f172a",
)
ax.set_xlabel("Dias Úteis de Trânsito", fontsize=11, labelpad=10, color="#475569")
ax.set_xlim(0, 25)
ax.invert_yaxis()  # Exibe o menor prazo no topo
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("grafico_tempo_entrega_estado.png", dpi=300)
plt.show()

# -----------------------------------------------------------------------------
# 3. GRÁFICO 2: SENSIBILIDADE DO REVIEW SCORE AO SLA DE ENTREGA
# -----------------------------------------------------------------------------
# Dados de degradação da nota média vs. cumprimento do prazo
dados_satisfacao = pd.DataFrame(
    {
        "Faixa_SLA": [
            "Entrega No Prazo",
            "Atraso de 1 a 3 Dias",
            "Atraso Superior a 7 Dias",
        ],
        "Review_Score": [4.43, 3.08, 1.18],
        "Cor": ["#16a34a", "#eab308", "#dc2626"],
    }
)

fig, ax = plt.subplots(figsize=(10, 5))

bars_sat = ax.bar(
    dados_satisfacao["Faixa_SLA"],
    dados_satisfacao["Review_Score"],
    color=dados_satisfacao["Cor"],
    width=0.45,
)

# Adicionando os valores numéricos acima das colunas
for bar in bars_sat:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f"{height:.2f} ★",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#0f172a",
    )

ax.set_title(
    "Pontuação Média (Review Score: 1 a 5) vs. Cumprimento do Prazo",
    fontsize=14,
    fontweight="bold",
    pad=20,
    color="#0f172a",
)
ax.set_ylabel("Review Score Médio", fontsize=11, labelpad=10, color="#475569")
ax.set_ylim(0, 5.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("grafico_review_score_sla.png", dpi=300)
plt.show()
