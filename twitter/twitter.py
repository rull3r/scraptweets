from bs4 import BeautifulSoup
import requests
import sys

def obtenerTuits(cuenta, twitter):
    """Con esta funcion obtendremos cadauno de los tuit que salen en la peticion inicial"""
    tuits = twitter.find_all("li", {"data-item-type": "tweet"})
    # print(tuits)
    i=0


if __name__ == "__main__":
    # print(sys.argv[1])

    cuenta = sys.argv[1]
    url = "http://www.twitter.com/" + cuenta
    twitter = requests.get(url)
    twitter = BeautifulSoup(twitter.content)
    if twitter.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Usuario Invalido :(")
    else:
        print("\n\n Usuario Encontrado :)")
    tweets = obtenerTuits(cuenta, twitter)