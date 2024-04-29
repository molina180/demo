from dash import Dash, html, dcc
import dash
import plotly.express as px
import dash_bootstrap_components as dbc

px.defaults.template = "ggplot2"

external_css = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "https://openai.com/style.css"
]

app = dash.Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, *external_css])

header = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Embed(src="/assets/header_logo.svg", height="120px"),
                    ]), className="d-inline-flex align-items-center"),
                ],
                align="center",
                style={"width": "100%"}  # Asegura que el header ocupe todo el ancho
            ),
            href="/",
        ),
    ],
    color="dark",
    dark=True,
)

# Contenedor principal que incluye el header y el contenido con un ancho máximo de 1200px
app.layout = html.Div([
    header,
    html.Div([
        html.Br(),
        html.Div([
            dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
                for page in dash.page_registry.values()
        ],
            className="containers",  # Limita el ancho del contenido a 1200px
            style={"max-width": "1200px", "margin": "auto"}  # Centra el contenido y le da un ancho máximo de 1200px
        ),
        dash.page_container
    ]),
    
    # Estilos CSS
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)