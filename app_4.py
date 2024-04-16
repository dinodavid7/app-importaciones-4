import pandas as pd
import sqlite3
import plotly.express as px
import dash
from dash import Dash, html, dcc

# Conexión a la base de datos
conn = sqlite3.connect('database.db')

# Consulta a la base de datos
query = "SELECT * FROM importaciones_pe"
importaciones_peru = pd.read_sql_query(query, conn)

# Preparación de los datos
importacion_peru = pd.melt(importaciones_peru, id_vars=['CONTINENTE', 'PAÍS DE ORIGEN'], var_name='AÑO',
                           value_name='IMPORTACION (millones de US$)')
importacion_peru['IMPORTACION (millones de US$)'] = importacion_peru['IMPORTACION (millones de US$)'] / 1e6
importacion_peru_evol = importacion_peru.groupby('AÑO')['IMPORTACION (millones de US$)'].sum().reset_index()

importacion_pais = importacion_peru.groupby(['CONTINENTE', 'PAÍS DE ORIGEN'])['IMPORTACION (millones de US$)'].sum().reset_index()
importacion_pais = importacion_pais.sort_values('IMPORTACION (millones de US$)', ascending=False)

importacion_pais_top_10 = importacion_pais.head(10)
importaciones_china_eeuu = importacion_peru[importacion_peru['PAÍS DE ORIGEN'].isin(['CHINA', 'ESTADOS UNIDOS'])]

# Cierre de la conexión a la base de datos
conn.close()

# Aplicación Dash para el Gráfico 4
app_graph4 = Dash(__name__)
server_graph4 = app_graph4.server

app_graph4.layout = html.Div([
    dcc.Graph(
        id='graph4',
        figure=px.line(
            data_frame=importaciones_china_eeuu,
            x='AÑO',
            y='IMPORTACION (millones de US$)',
            color='PAÍS DE ORIGEN',
            title='Gráfico 4 - Importaciones de China y EE.UU. a Perú (2005-2023)'
        ).update_layout(
            xaxis_title='Año',
            yaxis_title='Importación (millones de US$)',
            title_font=dict(size=24, family='Arial', color='black'),
            xaxis=dict(title_font=dict(size=18), tickangle=-45),
            yaxis=dict(title_font=dict(size=18)),
            legend_title='PAÍS',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=50, b=50)
        ).update_traces(mode='markers+lines', marker=dict(size=5))
    )
])

if __name__ == '__main__':
    app_graph4.run_server(debug=True)