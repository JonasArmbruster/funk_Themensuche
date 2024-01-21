import requests
from bs4 import BeautifulSoup


url = "https://www.funk.net/channel/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")



ziel_href_prefix = '/channel'
ziel_a_elements = soup.find_all('a', href=lambda value: value and value.startswith(ziel_href_prefix))


href_texts = [a_element.get('href') for a_element in ziel_a_elements]



# Benutzereingabe für den zu suchenden String
search = input("Geben Sie das gesuchte Stichwort ein: ")

for channel in href_texts:
    try:
        url = f"https://www.funk.net/{channel}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        page.raise_for_status()

        # Nach h2-Elementen suchen, die den Benutzereingabe-String enthalten (Alle Videobeschreibungen sind in h2-Elementen enthalten)
        video_titles = soup.find_all('h2', string=lambda string: string and search.lower() in string.lower())
        channel_names = soup.find('h1')

        # Ausgabe der gefundenen h2-Elemente
        if video_titles:
            print("Der Kanal '{}' enthält folgende Videos zu deinem Stichwort: {}".format(channel_names.string, [h2.string for h2 in video_titles]))
        else:
            pass
            
        for title in video_titles:
            aktuelles_element = title

             # Schleife, die bis zum dritten Eltern-Element geht
            for _ in range(3):
                aktuelles_element = aktuelles_element.find_parent()

            # Extrahiert den Link aus dem aktuell gespeicherten Eltern-Element
            link_text = aktuelles_element.get('href')
            # Ausgabe der extrahierten URL
            print("Hier kommst du zum Video: https://www.funk.net{}".format(link_text))


    except requests.exceptions.RequestException as e:
        print("Fehler beim Abrufen der Seite {}: {}".format(channel, e))




