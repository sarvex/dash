import dash
from dash import html, Input, Output, callback


dash.register_page(__name__, id="page1")

layout = html.Div(
    [
        html.Div("text for page1", id="text_page1"),
        html.Button("goto page2", id="btn1", n_clicks=0),
    ]
)


@callback(Output("url", "pathname"), Input("btn1", "n_clicks"))
def update(n):
    return "/page2" if n > 0 else dash.no_update
