from bs4 import BeautifulSoup
import requests
import sys
import lxml
import re 

# Algunas clases varian, asi que lo mejor es usar un expresion regular
clase = re.compile(r"tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet")
tiempo = re.compile(r"_timestamp")

def elementos(tuitAtributos):
    """Funcion que obtendra cada uno de los elementos de un tuit"""
  
    # Lista vacia que iremos llenando con los elementos de un tuit
    tuitElement=[]

    # Obtenemos el Id del tuit
    tuitElement.append(int(tuitAtributos.get("data-tweet-id")))

    #  Sabremos si es un retuit o no
    if tuitAtributos.has_attr('data-retweeter'):
        # En caso de serlo obtenderemos el id del tuit original
        tuitElement.append(tuitAtributos.has_attr('data-retweeter'))
        tuitElement.append(int(tuitAtributos.get("data-retweet-id")))
    else:
        # En caso de no serlo obtenderemos el id del tuit original como nan
        tuitElement.append(tuitAtributos.has_attr('data-retweeter'))
        tuitElement.append(float("nan"))

    # Obtenemos el twitter de la persona @
    tuitElement.append(tuitAtributos.find("span", {"class": "username u-dir u-textTruncate"}).get_text())

    # Obtenemos el Nombre de la cuenta de la persona que hizo el tuit o el retuit
    tuitElement.append(tuitAtributos.get("data-name"))

    # Id del usuario
    tuitElement.append(int(tuitAtributos.get("data-user-id")))

    # Obtenemos el url del avatar
    tuitElement.append(tuitAtributos.find("img", {"class": "avatar js-action-profile-avatar"})["src"])

    # Obtenermos el tiempo en formato timestamp
    tuitElement.append(int(tuitAtributos.find("span", {"class": tiempo})["data-time"]))

    # Obtenemos el tiempo en formato dato por twitter
    tuitElement.append(tuitAtributos.find("a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})["title"])

    # Obtenemos texto del tuit
    tuitElement.append(tuitAtributos.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).get_text())

    # Obtenemos Los mensajes, los retuit y los likes en ese orden
    estadisticas = tuitAtributos.find_all("span", {"class": "ProfileTweet-actionCount"})
    for i in range(3):
        tuitElement.append(estadisticas[i]["data-tweet-stat-count"])

    print(tuitElement)

def obtenerTuits(cuenta, twitter):
    """Con esta funcion obtendremos cadauno de los tuit que salen en la peticion inicial"""
    
    # Obtenemos el etiqueta que contiene todos los tuit que salen al hacer la consulta
    tuits = twitter.find_all("div", {"class": clase})

    # Iremos recorriendo cada tuit
    for tuit in tuits:
        elementos(tuit)

if __name__ == "__main__":

    try:
        # Para poder ingresar la variable al momento de ejecutar el script
        cuenta = sys.argv[1]
        url = "http://www.twitter.com/" + cuenta
        twitter = requests.get(url)
        twitter = BeautifulSoup(twitter.content, "lxml")
    except IndexError:
        print("No ingresaste un nombre valido")
        sys.exit(1)
    
    if twitter.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Usuario Invalido :(")
    else:
        print("\n\n Procediendo a recopilar todos los tuits del usuario @{} :)".format(cuenta))

    # Obtenemos todas las etiquetas dentro del html
    etiquetas = list(set([etiqueta.name for etiqueta in twitter.find_all()]))

    tweets = obtenerTuits(cuenta, twitter)