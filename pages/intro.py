import dash
from dash import html

dash.register_page(__name__, path='/', name="Introduction 🤓")


layout = html.Div(children=[
    html.Div(children=[
        html.H2("Social Media Scraper"),
        html.P("Hemos lanzado una nueva herramienta de scraping de redes sociales que está revolucionando la forma en que se obtienen datos en línea. Nuestra aplicación cuenta con un innovador script capaz de extraer datos de diversas plataformas sociales en cuestión de segundos, gracias a su integración con una API externa altamente eficiente."),
        html.Br(),
        html.P("Lo más emocionante es que nuestra herramienta no tiene límites restrictivos en cuanto al número de peticiones que puedes realizar. A diferencia de otras soluciones en el mercado, puedes aprovechar al máximo su funcionalidad sin preocuparte por restricciones arbitrarias. ¡Extrae datos sin límites y sin demoras!"),
        html.Br(),
        html.P("Además, nuestra herramienta no solo se destaca por su velocidad y versatilidad, sino también por su capacidad para adaptarse a tus necesidades específicas. Con un dashboard intuitivo y flexible, puedes analizar los datos extraídos de manera eficiente y personalizada."),
        html.Br(),
        html.P("Y eso no es todo, estamos comprometidos a seguir mejorando nuestra herramienta. En futuras versiones, planeamos agregar funciones de búsqueda avanzada en la red, lo que te permitirá obtener información aún más detallada y relevante."),
        html.Br(),
        html.P("¡Aprovecha esta oportunidad para descubrir una nueva era en el scraping de redes sociales! 🚀"),
        html.Br(),
        html.Img(src='/assets/logo_info.png', className="json-image", style={'max-width': '300px', 'display': 'block', 'margin': 'auto'})
    ],
    style={'max-width': '1000px', 'margin': 'auto'})  # Aplicando el estilo de ancho máximo de 1200px y centrado
], className="bg-light p-4 m-2")  # Estilo adicional de fondo, padding y margen
