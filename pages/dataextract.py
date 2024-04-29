import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from .data_extraction import extract_facebook_data, extract_instagram_data, extract_tiktok_data, extract_twitter_data, extract_youtube_data


dash.register_page(__name__, path='/dataextract', name="Scraping data 🕷️")


layout = html.Div([
    html.H1("Extraer Data", className="text-center mb-4"),  # Encabezado principal
    html.Div([
        html.Div([
            html.Img(src='/assets/facebook_logo.png', className="logo", style={"vertical-align": "middle"}),  # Logo
            html.Label("Facebook Data", className="fw-bold mb-2 label", style={"margin-left": "10px"}),  # Título de sección con margen izquierdo de 5px
            dcc.Checklist(id="facebook-checkbox", options=[{"label": "", "value": "facebook"}], style={"font-size": "20px"}),  # Checkbox más grande y con margen izquierdo de 5px  # Lista de verificación
            html.Label("URL de Facebook:", className="label"),
            dcc.Input(id="facebook-start-url-input", type="text", placeholder="Ingrese la URL de inicio", className="form-control mb-2", style={"max-width": "450px"}),  # Entrada de texto
            html.Label("Límite de resultados (Facebook):", className="label"),
            dcc.Input(id="facebook-results-limit-input", type="number", placeholder="Ingrese el límite de resultados", className="form-control", style={"max-width": "450px"}),
        ], className="containers"),  # Contenedor
    ]),
    html.Div([
        html.Div([
            html.Img(src='/assets/instagram_logo.png', className="logo", style={"vertical-align": "middle"}),  # Logo con ajuste de alineación vertical
            html.Label("Instagram Data", className="fw-bold mb-2 label", style={"margin-left": "10px"}),
            dcc.Checklist(id="instagram-checkbox", options=[{"label": "", "value": "instagram"}], style={"font-size": "20px"}),  # Lista de verificación
            html.Label("URL de Instagram:", className="label"),
            dcc.Input(id="instagram-start-url-input", type="text", placeholder="Ingrese la URL de inicio", className="form-control mb-2", style={"max-width": "450px"}),  # Entrada de texto
            html.Label("Límite de resultados (Instagram):", className="label"),
            dcc.Input(id="instagram-results-limit-input", type="number", placeholder="Ingrese el límite de resultados", className="form-control", style={"max-width": "450px"}),
        ], className="containers"),  # Contenedor
    ]),
    html.Div([
        html.Div([
            html.Img(src='/assets/tiktok_logo.png', className="logo", style={"vertical-align": "middle"}), 
            html.Label("TikTok Data", className="fw-bold mb-2 label", style={"margin-left": "10px"}),  # Título de sección
            dcc.Checklist(id="tiktok-checkbox", options=[{"label": "", "value": "tiktok"}], style={"font-size": "20px"}),  # Lista de verificación
            html.Label("Perfil TikTok:", className="label"),
            dcc.Input(id="tiktok-start-url-input", type="text", placeholder="Ingrese el usuario", className="form-control mb-2", style={"max-width": "450px"}),  # Entrada de texto
            html.Label("Límite de resultados (TikTok):", className="label"),
            dcc.Input(id="tiktok-results-limit-input", type="number", placeholder="Ingrese el límite de resultados", className="form-control", style={"max-width": "450px"}),
        ], className="containers"),  # Contenedor
    ]),
    html.Div([
        html.Div([
            html.Img(src='/assets/x_logo.png', className="logo", style={"vertical-align": "middle"}),
            html.Label("Twitter Data", className="fw-bold mb-2 label", style={"margin-left": "10px"}),  # Título de sección
            dcc.Checklist(id="twitter-checkbox", options=[{"label": "", "value": "twitter"}], style={"font-size": "20px"}),  # Lista de verificación
            html.Label("URL de Twitter:", className="label"),
            dcc.Input(id="twitter-start-url-input", type="text", placeholder="Ingrese la URL de inicio", className="form-control mb-2", style={"max-width": "450px"}),  # Entrada de texto
            html.Label("Límite de resultados (Twitter):", className="label"),
            dcc.Input(id="twitter-results-limit-input", type="number", placeholder="Ingrese el límite de resultados", className="form-control", style={"max-width": "450px"}),
        ], className="containers"),  # Contenedor
    ]),
    html.Div([
        html.Div([
            html.Img(src='/assets/youtube_logo.png', className="logo", style={"vertical-align": "middle"}),
            html.Label("Youtube Data", className="fw-bold mb-2 label", style={"margin-left": "10px"}),
            dcc.Checklist(id="youtube-checkbox", options=[{"label": "", "value": "twitter"}], style={"font-size": "20px"}),  # Lista de verificación
            html.Label("Palabra a buscar:", className="label"),
            dcc.Input(id="youtube-start-url-input", type="text", placeholder="Ingrese la palabra a buscar", className="form-control mb-2", style={"max-width": "450px"}),  # Entrada de texto
            html.Label("Límite de resultados (Youtube):", className="label"),
            dcc.Input(id="youtube-results-limit-input", type="number", placeholder="Ingrese el límite de resultados", className="form-control", style={"max-width": "450px"}),
        ], className="containers"),  # Contenedor
    ]),
    html.Div([
        html.Div([
            html.Button("Extraer Datos", id="extract-button", className="btn btn-dark m-2"),  # Botón de extracción
            html.Div(id="extraction-status", className="fw-bold text-center text-primary")  # Estado de la extracción
        ], className="buttons"),  # Contenedor de botones
    ]),
    
    # Estilos CSS
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    )
])


# Callback para manejar la extracción de datos
@callback(
    Output("extraction-status", "children"),
    [Input("extract-button", "n_clicks")],
    [
        State("facebook-checkbox", "value"),
        State("facebook-start-url-input", "value"),
        State("facebook-results-limit-input", "value"),
        State("instagram-checkbox", "value"),
        State("instagram-start-url-input", "value"),
        State("instagram-results-limit-input", "value"),
        State("tiktok-checkbox", "value"),
        State("tiktok-start-url-input", "value"),
        State("tiktok-results-limit-input", "value"),
        State("twitter-checkbox", "value"),
        State("twitter-start-url-input", "value"),
        State("twitter-results-limit-input", "value"),
        State("youtube-checkbox", "value"),
        State("youtube-start-url-input", "value"),
        State("youtube-results-limit-input", "value")
    ]
)

def extract_data(n_clicks, facebook_checkbox, facebook_start_url, facebook_results_limit,
                 instagram_checkbox, instagram_start_url, instagram_results_limit,
                 tiktok_checkbox, tiktok_start_url, tiktok_results_limit, twitter_checkbox, 
                 twitter_start_url, twitter_results_limit, youtube_checkbox, youtube_start_url,
                 youtube_results_limit):
    
    if n_clicks:
        extraction_status = []
        
        # Verifica si el checkbox de Facebook está seleccionado y todos los campos requeridos están llenos
        if facebook_checkbox and facebook_start_url and facebook_results_limit:
            df_path = extract_facebook_data(start_url=facebook_start_url, results_limit=int(facebook_results_limit))
            extraction_status.append(f"Extracción de datos de Facebook completada. Guardado en: {df_path}")
            
        # Verifica si el checkbox de Instagram está seleccionado y todos los campos requeridos están llenos
        if instagram_checkbox and instagram_start_url and instagram_results_limit:
            df_path = extract_instagram_data(start_url=instagram_start_url, results_limit=int(instagram_results_limit))
            extraction_status.append(f"Extracción de datos de Instagram completada. Guardado en: {df_path}")
            
        # Verifica si el checkbox de TikTok está seleccionado y todos los campos requeridos están llenos
        if tiktok_checkbox and tiktok_start_url and tiktok_results_limit:
            df_path = extract_tiktok_data(start_url=tiktok_start_url, results_limit=int(tiktok_results_limit))
            extraction_status.append(f"Extracción de datos de TikTok completada. Guardado en: {df_path}")
            
        # Verifica si el checkbox de Twitter está seleccionado y todos los campos requeridos están llenos
        if twitter_checkbox and twitter_start_url and twitter_results_limit:
            df_path = extract_twitter_data(start_url=twitter_start_url, results_limit=int(twitter_results_limit))
            extraction_status.append(f"Extracción de datos de Twitter completada. Guardado en: {df_path}")
        
        # Verifica si el checkbox de Youtube está seleccionado y todos los campos requeridos están llenos
        if youtube_checkbox and youtube_start_url and youtube_results_limit:
            df_path = extract_youtube_data(start_url=youtube_start_url, results_limit=int(youtube_results_limit))
            extraction_status.append(f"Extracción de datos de Youtube completada. Guardado en: {df_path}")
            
        # Devuelve los mensajes de estado de extracción concatenados en una sola cadena
        if extraction_status:
            return "\n".join(extraction_status)
        else:
            return "Seleccione al menos una opción de extracción y complete los campos correspondientes."
    else:
        return ""


