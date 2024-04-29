import re
import json
import os
from apify_client import ApifyClient
import pandas as pd

def extract_facebook_data(start_url, results_limit):
    # Definir una función para limpiar texto
    def clean_text(text):
        # Remover emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                                   u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                                   u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        cleaned_text = emoji_pattern.sub(r'', text)
        # Remover enlaces
        cleaned_text = re.sub(r'http\S+', '', cleaned_text)
        # Remover hashtags y menciones
        cleaned_text = re.sub(r'#\w+', '', cleaned_text)
        cleaned_text = re.sub(r'@\w+', '', cleaned_text)
        return cleaned_text.strip()

    # Definir una función para extraer emojis de un texto
    def extract_emojis(text):
        # Compilar el patrón de emojis
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                               u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                               u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
        # Encontrar emojis en el texto y devolverlos como una lista
        emojis = emoji_pattern.findall(text)
        return [emoji.encode('unicode_escape').decode('utf-8') for emoji in emojis]

    # Definir función para extraer hashtags
    def extract_hashtags(text):
        # Patrón para buscar hashtags
        hashtag_pattern = re.compile(r'#\w+')
        # Encontrar todos los hashtags en el texto
        hashtags = hashtag_pattern.findall(text)
        return hashtags

    # Inicializar el cliente de Apify con tu token API
    client = ApifyClient("apify_api_fTp8FnZ6gW9cJiuGiixgylk9CcuiO82rRl1Q")

    # Preparar la entrada del Actor
    run_input = {
        "startUrls": [{ "url": start_url }],
        "resultsLimit": results_limit,
    }

    run = client.actor("KoJrdxJCTtpon81KY").call(run_input=run_input)

    data = []

    # Iterar sobre los elementos y agregar los datos relevantes a la lista
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():  
        # Agregar la columna "cleanText"
        clean_caption = clean_text(item["text"]).replace('\n', '')  # Eliminar saltos de línea
        clean_caption = clean_caption.replace('\n', '')  # Eliminar saltos de línea adicionales
        emojis = extract_emojis(item["text"])
        hashtags = extract_hashtags(item["text"])
        
        # Verificar si la clave "comments" está presente en el diccionario "item"
        if "comments" in item:
            comments_count = item["comments"]
        else:
            comments_count = 0  # O cualquier otro valor por defecto que desees
        
        data.append({
            "inputUrl": item["facebookUrl"],
            "shortCode": item["postId"],
            "caption": item["text"].replace('\n', ''),
            "hashtags": hashtags,
            "shares": item["shares"],
            "commentsCount": comments_count,  # Usar la variable comments_count
            "likesCount": item["likes"],
            "timestamp": item["time"],
            "isSponsored": item["pageAdLibrary"]["is_business_page_active"],
            "cleanText": clean_caption,
            "emojis": emojis
        })

    # Obtener la ruta completa del archivo JSON
    ruta_json = os.path.join('data', 'facebook_page.json')

    # Guardar los datos en el archivo JSON
    with open(ruta_json, 'w', encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4)

    return ruta_json



def clean_instagram_url(url):
    # Eliminar cualquier carácter al final de la URL
    url = url.strip()
    # Verificar si la URL ya contiene "https://www.instagram.com/"
    if url.startswith("https://www.instagram.com/"):
        return url
    # Agregar "https://www.instagram.com/" al principio si no está presente
    else:
        return "https://www.instagram.com/" + url.strip("/")


def extract_instagram_data(start_url, results_limit):
    
    # Definir una función para limpiar texto
    def clean_text(text):
        # Remover emojis
        emoji_pattern = re.compile("["
                                    u"\U0001F600-\U0001F64F"  # emoticons
                                    u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                                    u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                                    u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                                    u"\U00002702-\U000027B0"
                                    u"\U000024C2-\U0001F251"
                                    "]+", flags=re.UNICODE)
        cleaned_text = emoji_pattern.sub(r'', text)
        # Remover enlaces
        cleaned_text = re.sub(r'http\S+', '', cleaned_text)
        # Remover hashtags y menciones
        cleaned_text = re.sub(r'#\w+', '', cleaned_text)
        cleaned_text = re.sub(r'@\w+', '', cleaned_text)
        return cleaned_text.strip()


    # Definir una función para extraer emojis de un texto
    def extract_emojis(text):
        # Compilar el patrón de emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                            u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        # Encontrar emojis en el texto y devolverlos como una lista
        emojis = emoji_pattern.findall(text)
        return [emoji.encode('unicode_escape').decode('utf-8') for emoji in emojis]


    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_fTp8FnZ6gW9cJiuGiixgylk9CcuiO82rRl1Q")

    # Prepare the Actor input
    run_input = {
        "directUrls": [start_url],
        "resultsType": "posts",
        "resultsLimit": results_limit,
        "searchType": "hashtag",
        "searchLimit": 1,
        "addParentData": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

    data = []

    # Iterar sobre los elementos y agregar los datos relevantes a la lista
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Agregar la columna "cleanText"
        clean_caption = clean_text(item["caption"])
        emojis = extract_emojis(item["caption"])
        
        data.append({
            "inputUrl": item["inputUrl"],
            "type": item["type"],
            "shortCode": item["shortCode"],
            "caption": item["caption"],
            "hashtags": item["hashtags"],
            "mentions": item["mentions"],
            "commentsCount": item["commentsCount"],
            "likesCount": item["likesCount"],
            "timestamp": item["timestamp"],
            "isSponsored": item["isSponsored"],
            "cleanText": clean_caption,
            "emojis": emojis
        })

    # Crear un DataFrame a partir de la lista de datos
    df = pd.DataFrame(data)
    #print(df)

    ruta_json = os.path.join('data', 'instagram_page.json')

    # Guardar los datos en el archivo JSON
    with open(ruta_json, 'w', encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4)
    
    return ruta_json

def extract_tiktok_data(start_url, results_limit):
        # Definir una función para limpiar texto
    def clean_text(text):
        # Remover emojis
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                                u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                                u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
        cleaned_text = emoji_pattern.sub(r'', text)
        # Remover enlaces
        cleaned_text = re.sub(r'http\S+', '', cleaned_text)
        # Remover hashtags y menciones
        cleaned_text = re.sub(r'#\w+', '', cleaned_text)
        cleaned_text = re.sub(r'@\w+', '', cleaned_text)
        return cleaned_text.strip()


    # Definir una función para extraer emojis de un texto
    def extract_emojis(text):
        # Compilar el patrón de emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                            u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        # Encontrar emojis en el texto y devolverlos como una lista
        emojis = emoji_pattern.findall(text)
        return [emoji.encode('unicode_escape').decode('utf-8') for emoji in emojis]


    # Definir función para extraer hashtags
    def extract_hashtags(text):
        # Patrón para buscar hashtags
        hashtag_pattern = re.compile(r'#\w+')
        # Encontrar todos los hashtags en el texto
        hashtags = hashtag_pattern.findall(text)
        return hashtags


    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_fTp8FnZ6gW9cJiuGiixgylk9CcuiO82rRl1Q")

    # Prepare the Actor input
    run_input = {
        "profiles": [start_url],
        "resultsPerPage": results_limit,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("0FXVyOXXEmdGcV88a").call(run_input=run_input)

    data = []

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Agregar la columna "cleanText"
        clean_caption = clean_text(item["text"]).replace('\n', '')  # Eliminar saltos de línea
        clean_caption = clean_caption.replace('\n', '')  # Eliminar saltos de línea adicionales
        emojis = extract_emojis(item["text"])
        hashtags = extract_hashtags(item["text"])
        
        
        data.append({
            "inputUrl": item["authorMeta"]["name"],
            "shortCode": item["id"],
            "caption": item["text"],
            "hashtags": hashtags,
            "shares": item["shareCount"],
            "commentsCount": item["commentCount"],  # Usar la variable comments_count
            "likesCount": item["diggCount"],
            "playCount": item["playCount"],
            "collectCount": item["collectCount"],
            "timestamp": item["createTimeISO"],
            "isSponsored": item["authorMeta"]["commerceUserInfo"]["commerceUser"],
            "cleanText": clean_caption,
            "emojis": emojis
        })


    # Crear un DataFrame a partir de la lista de datos
    df = pd.DataFrame(data)
    #print(df)

    ruta_json = os.path.join('data', 'tiktok_page.json')

    # Guardar los datos en el archivo JSON
    with open(ruta_json, 'w', encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4)
        
    return ruta_json


def extract_twitter_data(start_url, results_limit):
        # Definir una función para limpiar texto
    def clean_text(text):
        # Remover emojis
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                                u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                                u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
        cleaned_text = emoji_pattern.sub(r'', text)
        # Remover enlaces
        cleaned_text = re.sub(r'http\S+', '', cleaned_text)
        # Remover hashtags y menciones
        cleaned_text = re.sub(r'#\w+', '', cleaned_text)
        cleaned_text = re.sub(r'@\w+', '', cleaned_text)
        return cleaned_text.strip()


    # Definir una función para extraer emojis de un texto
    def extract_emojis(text):
        # Compilar el patrón de emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                            u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        # Encontrar emojis en el texto y devolverlos como una lista
        emojis = emoji_pattern.findall(text)
        return [emoji.encode('unicode_escape').decode('utf-8') for emoji in emojis]


    # Definir función para extraer hashtags
    def extract_hashtags(text):
        # Patrón para buscar hashtags
        hashtag_pattern = re.compile(r'#\w+')
        # Encontrar todos los hashtags en el texto
        hashtags = hashtag_pattern.findall(text)
        return hashtags

    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_fTp8FnZ6gW9cJiuGiixgylk9CcuiO82rRl1Q")

    # Prepare the Actor input
    run_input = {
        "addNotFoundUsersToOutput": False,
        "addUserInfo": True,
        "customMapFunction": "(object) => { return {...object} }",
        "maxTweetsPerUser": results_limit,
        "onlyUserInfo": False,
        "proxy": {
            "useApifyProxy": True
        },
        "startUrls": [start_url]
    }


    run = client.actor("wbpC5fjeAxy06bonV").call(run_input=run_input)


    data = []

    # Iterar sobre los elementos y agregar los datos relevantes a la lista
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():  
        # Agregar la columna "cleanText"
        clean_caption = clean_text(item["full_text"]).replace('\n', '')  # Eliminar saltos de línea
        clean_caption = clean_caption.replace('\n', '')  # Eliminar saltos de línea adicionales
        emojis = extract_emojis(item["full_text"])
        hashtags = extract_hashtags(item["full_text"])
        
        # # Verificar si la clave "comments" está presente en el diccionario "item"
        # if "comments" in item:
        #     comments_count = item["reply_count"]
        # else:
        #     comments_count = 0  # O cualquier otro valor por defecto que desees
        
        data.append({
            "inputUrl": item["user"]["screen_name"],
            "shortCode": item["id_str"],
            "caption": item["full_text"].replace('\n', ''),
            "hashtags": hashtags,
            "shares": item["retweet_count"],
            "commentsCount": item["reply_count"],  # Usar la variable comments_count
            "likesCount": item["favorite_count"],
            "timestamp": item["created_at"],
            "isSponsored": item["is_quote_status"],
            "cleanText": clean_caption,
            "emojis": emojis
        })


    # Crear un DataFrame a partir de la lista de datos
    df = pd.DataFrame(data)
    #print(df)

    # Obtener la ruta completa del archivo JSON
    ruta_json = os.path.join('data', 'twitter_page.json')

    # Guardar los datos en el archivo JSON
    with open(ruta_json, 'w', encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4)
        
    return ruta_json


def extract_youtube_data(start_url, results_limit):
        # Definir una función para limpiar texto
    def clean_text(text):
        # Remover emojis
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                                u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                                u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
        cleaned_text = emoji_pattern.sub(r'', text)
        # Remover enlaces
        cleaned_text = re.sub(r'http\S+', '', cleaned_text)
        # Remover hashtags y menciones
        cleaned_text = re.sub(r'#\w+', '', cleaned_text)
        cleaned_text = re.sub(r'@\w+', '', cleaned_text)
        return cleaned_text.strip()


    # Definir una función para extraer emojis de un texto
    def extract_emojis(text):
        # Compilar el patrón de emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                            u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        # Encontrar emojis en el texto y devolverlos como una lista
        emojis = emoji_pattern.findall(text)
        return [emoji.encode('unicode_escape').decode('utf-8') for emoji in emojis]


    # Definir función para extraer hashtags
    def extract_hashtags(text):
        # Patrón para buscar hashtags
        hashtag_pattern = re.compile(r'#\w+')
        # Encontrar todos los hashtags en el texto
        hashtags = hashtag_pattern.findall(text)
        return hashtags

    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_fTp8FnZ6gW9cJiuGiixgylk9CcuiO82rRl1Q")

    # Prepare the Actor input
    run_input = {
        "downloadSubtitles": False,
        "hasCC": False,
        "hasLocation": False,
        "hasSubtitles": False,
        "is360": False,
        "is3D": False,
        "is4K": False,
        "isBought": False,
        "isHD": False,
        "isHDR": False,
        "isLive": False,
        "isVR180": False,
        "maxResultStreams": 0,
        "maxResults": results_limit,
        "maxResultsShorts": 0,
        "preferAutoGeneratedSubtitles": False,
        "saveSubsToKVS": False,
        "searchKeywords": start_url,
        "startUrls": [],
        "subtitlesLanguage": "any",
        "subtitlesFormat": "srt"
    }

    run = client.actor("h7sDV53CddomktSi5").call(run_input=run_input)


    data = []

    # Iterar sobre los elementos y agregar los datos relevantes a la lista
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():  
        # Agregar la columna "cleanText"
        clean_caption = clean_text(item["text"]).replace('\n', '')  # Eliminar saltos de línea
        clean_caption = clean_caption.replace('\n', '')  # Eliminar saltos de línea adicionales
        emojis = extract_emojis(item["text"])
        hashtags = extract_hashtags(item["text"])
        
        # Verificar si la clave "comments" está presente en el diccionario "item"
        if "comments" in item:
            comments_count = item["commentsCount"]
        else:
            comments_count = 0  # O cualquier otro valor por defecto que desees
        
        data.append({
            "inputUrl": item["url"],
            "shortCode": item["id"],
            "caption": item["text"].replace('\n', ''),
            "hashtags": hashtags,
            "shares": item["viewCount"],
            "commentsCount": comments_count,  # Usar la variable comments_count
            "likesCount": item["likes"],
            "timestamp": item["date"],
            "isSponsored": item["channelName"],
            "cleanText": clean_caption,
            "emojis": emojis
        })


    # Crear un DataFrame a partir de la lista de datos
    df = pd.DataFrame(data)
    #print(df)

    # Obtener la ruta completa del archivo JSON
    ruta_json = os.path.join('data', 'youtube_page.json')

    # Guardar los datos en el archivo JSON
    with open(ruta_json, 'w', encoding="UTF-8") as json_file:
        json.dump(data, json_file, indent=4)
    
    return ruta_json