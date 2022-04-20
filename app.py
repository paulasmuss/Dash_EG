import dash
import dash_design_kit as ddk
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)
server = app.server  # expose server variable for Procfile

df = px.data.stocks()

app.layout = ddk.App([
    ddk.Header([
        ddk.Logo(src=app.get_asset_url('logo.png')),
        ddk.Title('Dash Enterprise Sample Application'),
    ]),
    ddk.Row(children=[
        ddk.Card(children=[
            ddk.CardHeader(children=[
                dcc.Dropdown(
                    id='title-dropdown',
                    options=[{'label': i, 'value': i}
                        for i in ['GOOG', 'AAPL', 'AMZN']],
                    value='GOOG'
                )
            ]),
            ddk.Graph(id='update-graph', style={'height':300}),
        ]),
    ]),

    ddk.Row(children=[
        ddk.Card(width=50, children=ddk.Graph(figure=px.line(df, x="date", y=["AMZN", "FB"], title='Stock Prices Crap'))),

        ddk.Card(width=50, children=ddk.Graph(figure=px.line(df, x="date", y=["AAPL", "MSFT"], title='Stock Prices Others')))
    ])
])


@app.callback(Output('update-graph', 'figure'),
              [Input('title-dropdown', 'value')])
def update_graph(value):
    if value == 'GOOG':
        return px.line(df, x="date", y="GOOG", title='goggles Stock Price')
    elif value == 'AAPL':
        return px.line(df, x="date", y="AAPL", title='Pear Stock Price')
    elif value == 'AMZN':
        return px.line(df, x="date", y="AMZN", title='Amazon Chicken Stock Price')

if __name__ == '__main__':
    app.run_server(debug=True)
