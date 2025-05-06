from dash import Input, Output
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

def register_elenco_callbacks(app):
    @app.callback(
        Output('tabela-jogadores', 'data'),
        [Input('dropdown-posicao', 'value'),
         Input('dropdown-categoria', 'value'),
         Input('dropdown-ano', 'value')]
    )
    def update_table(posicao, categoria, ano):
        atletas_df = pd.read_excel('data/atletas.xlsx')
        filtered_df = atletas_df[atletas_df['Posição'] == posicao]
        if 'KPI' in filtered_df.columns:
            filtered_df['KPI'] = filtered_df['KPI'].round(0).astype(int)
        return filtered_df.to_dict('records')

    @app.callback(
        Output('grafico-distribuicao-kpi', 'figure'),
        [Input('dropdown-posicao', 'value')]
    )
    def update_kpi_distribution(posicao):
        u17_df = pd.read_excel('data/u17br.xlsx')
        atletas_df = pd.read_excel('data/atletas.xlsx')

        df_geral = u17_df[u17_df["Posição"] == posicao].copy()
        df_geral["KPI"] = pd.to_numeric(df_geral["KPI"], errors="coerce")
        kpis_gerais = df_geral["KPI"].dropna()

        df_sfera = atletas_df[atletas_df["Posição"] == posicao].copy()
        df_sfera["KPI"] = pd.to_numeric(df_sfera["KPI"], errors="coerce")
        kpis_sfera = df_sfera["KPI"].dropna()

        media = kpis_gerais.mean()
        desvio = kpis_gerais.std()
        x_vals = np.linspace(media - 3*desvio, media + 3*desvio, 500)
        y_vals = norm.pdf(x_vals, media, desvio)

        fig_kpi = go.Figure()

        fig_kpi.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode="lines",
            name="Distribuição",
            line=dict(color="#3CBBB1", width=2)
        ))
        fig_kpi.add_trace(go.Scatter(
            x=[x_vals.min(), x_vals.max()],
            y=[0, 0],
            mode="lines",
            line=dict(color="#C0C0C0", width=1),
            showlegend=False
        ))
        fig_kpi.add_trace(go.Scatter(
            x=kpis_gerais,
            y=[0] * len(kpis_gerais),
            mode="markers",
            marker=dict(size=8, color='rgba(255, 255, 255, 0.2)'),
            name="Brasileiro sub-17",
            hoverinfo="skip"
        ))
        fig_kpi.add_trace(go.Scatter(
            x=kpis_sfera,
            y=[0] * len(kpis_sfera),
            mode="markers",
            marker=dict(size=10, color="#3CBBB1"),
            name="Sfera sub-17",
            text=df_sfera["Jogador"],
            hovertemplate="%{text}<br>KPI: %{x:.2f}<extra></extra>"
        ))

        fig_kpi.update_layout(
            title=dict(
                text="Distribuição do desempenho por posição",
                x=0.5,
                y=0.95,
                font=dict(size=14, color="#C0C0C0", family="Arial Black")
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=260,
            font=dict(size=10, color="white"),
            xaxis=dict(showgrid=False, zeroline=False, color="white"),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="right",
                x=1,
                font=dict(size=10, color="white")
            )
        )

        return fig_kpi
