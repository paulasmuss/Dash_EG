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
                    inline=True,
                    style={'marginRight': 1000}
                )
            ]),
            ddk.Graph(id='update-graph', style={'height':300}),
        ]),
    ]),

    #ddk.Row(children=[
    #    ddk.Card(width=50, children=ddk.Graph(figure=px.line(df, x="date", y=["AMZN", "FB"], title='Storck Prices'))),
#
    #    ddk.Card(width=50, children=ddk.Graph(figure=px.line(df, x="date", y=["AAPL", "MSFT"], title='Stock Prices')))
    #])
])


@app.callback(Output('update-graph', 'figure'),
              [Input('chosen_year', 'value')])
def update_graph(chosen_year):
    print(chosen_year)
    chosen_year.sort()
    print('sorted: ', chosen_year)
    #if value == 'GOOG':
    #    return px.line(df, x="date", y="GOOG", title='goggles Stock Price')
    #elif value == 'AAPL':
    #    return px.line(df, x="date", y="AAPL", title='Apple Stock Price')
    #elif value == 'AMZN':
    #    return px.line(df, x="date", y="AMZN", title='Amazon Stock Price')

if __name__ == '__main__':
    app.run_server(debug=True, port=6667, proxy="http://0.0.0.0:6667::https://dash-signal-iduna.plotly.host")