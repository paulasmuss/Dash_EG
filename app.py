import dash
import dash_design_kit as ddk
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
server = app.server # expose server variable for Procfile

#df = px.data.stocks()
df = pd.read_excel("assets/GuVAuszug_RandomDatenExport.xlsx")
df = df.drop(columns= ['Sortierung_3'])

app.layout = ddk.App([
    ddk.Header([
        #ddk.Logo(src=app.get_asset_url('logo.png')),
        ddk.Title('Test GuV: Randomisierte Dateneinträge'),
    ]),
    ddk.Row(children=[
        ddk.Card(children=[
            ddk.CardHeader(title='Geschäftsjahr auswählen', children=[
                dcc.Checklist(
                    id='chosen_year',
                    options=[{'label': x, 'value': x, 'title': 'Auswahl Geschäftsjahr'}
                             for x in df['Jahr'].unique().tolist()],
                    value=[],
                    inline=True
                    )
            ]),
            ddk.Graph(id='update-graph', style={'height':300}),
        ])
    ])
])


@app.callback(Output('update-graph', 'figure'),
              [Input('chosen_year', 'value')])
def update_graph(chosen_year):
    chosen_year.sort()
    df_1 = df.groupby(['Jahr']).sum()
    df_1 = df_1.loc[chosen_year]

    df_2 = df.groupby(['Jahr', 'Ebene1']).sum()
    df_2 = df_2.unstack()
    df_2.columns = df_2.columns.droplevel()
        
    x_label = ['Verdiente Beiträge <br>für eigene Rechnung',
               'Beiträge aus der<br> Brutto-Rückstellung <br>für Beitragsrückerst.',
               'Erträge <br> aus Kapitalanlagen',
               'Nicht realisierte <br>Gewinne aus <br>Kapitalanlagen',
               'Sonstige <br>versicherungstechnische <br>Erträge f.e.R.',
               'Aufwendungenfür <br>Versicherungsfälle <br>für eigene Rechnung',
               'Veränder. <br>der übr. <br>versicherungstechn. <br>Netto-Rückstellungen'
               'Aufw. für <br> erfolgsabh.und<br> erfolgsunabh. <br>Beitragsrückerst. <br> f.e.R.',
               'Aufwendungen für <br>den <br>Versicherungsbetrieb <br>f.e.R.',
               'Aufwendungen für <br>Kapitalanlagen',
               'Nicht realisierte <br>Verluste aus Kapitalanlagen',
               'Sonstige <br>versicherungstechnische <br>Aufwendungen f.e.R.',
               'Versicherungstechnisches <br>Ergebnis für eigene Rechnung' ]

    #fig_2 = go.Figure()
    #for jahr in choosen_year:
    #    fig_2.add_trace(go.Bar(name=jahr, x=x_label, y=df_2.loc[int(jahr)]))
    #fig_2.update_layout(barmode='group', xaxis_tickangle=0)

    return [
        px.bar(x=df_1.index, y=df_1['Betrag']),
        #dcc.Graph(figure=fig_2)
    ]

if __name__ == '__main__':
    app.run_server(debug=True, port=6667, proxy="http://0.0.0.0:6667::https://dash-signal-iduna.plotly.host")