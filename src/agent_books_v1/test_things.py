import json
import os
import requests
from bs4 import BeautifulSoup

import dotenv
dotenv.load_dotenv()

class RedditOpinionSearch:
    def __init__(self):
        # Asegúrate de tener tu clave de API de Serper en las variables de entorno
        self.api_key = os.getenv('SERPER_API_KEY')
        self.url = "https://google.serper.dev/search"
    
    def search_reddit_opinions(self, book_title: str) -> str:
        """Busca opiniones en Reddit sobre un libro específico."""
        query = f"{book_title} book opinions site:reddit.com"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }
        
        # Realiza la solicitud a la API de Serper
        response = requests.post(self.url, headers=headers, data=payload)
        
        if response.status_code != 200:
            return f"Error al obtener los resultados de búsqueda: {response.status_code}"

        # Analiza la respuesta
        results = response.json().get('organic', [])
        reddit_links = [result['link'] for result in results if 'reddit.com' in result['link']]

        if not reddit_links:
            return f"No se encontraron opiniones en Reddit para '{book_title}'"

        # Extrae opiniones de las páginas de Reddit
        opinions = []
        for link in reddit_links:
            opinion = self.scrape_reddit_page(link)
            if opinion:
                opinions.append(f"Desde: {link}\n{opinion}")

        return "\n\n".join(opinions) if opinions else f"No se encontraron opiniones en Reddit para '{book_title}'"

    def scrape_reddit_page(self, link: str) -> str:
        """Extrae opiniones de una página de Reddit."""
        try:
            # Realiza la solicitud a la página de Reddit
            reddit_response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            reddit_soup = BeautifulSoup(reddit_response.text, 'html.parser')
            
            # Extrae comentarios (ajusta según la estructura HTML actual de Reddit)
            comments = []
            for comment in reddit_soup.find_all('div', class_='md'):
                text = comment.get_text(strip=True)
                if text:
                    comments.append(text)
            
            return "\n".join(comments[:5]) if comments else "No se encontraron comentarios."
        except Exception as e:
            return f"Error al extraer la página: {str(e)}"

# Script de prueba
"""if __name__ == "__main__":
    # Inicializa la clase
    searcher = RedditOpinionSearch()
    
    # Define el título del libro para buscar
    book_title = "The Catcher in the Rye"
    
    # Realiza la búsqueda
    result = searcher.search_reddit_opinions(book_title)
    
    # Imprime el resultado
    print(result)
"""


import json
import os
import requests
from bs4 import BeautifulSoup

import dotenv
dotenv.load_dotenv()



class RedditOpinionSearch:
    def __init__(self):
        # Asegúrate de tener tu clave de API de Serper en las variables de entorno
        self.api_key = os.getenv('SERPER_API_KEY')
        self.url = "https://google.serper.dev/search"
    
    def search_reddit_opinions(self, book_title: str) -> str:
        """Busca opiniones en Reddit sobre un libro específico."""
        query = f"{book_title} book opinions site:reddit.com"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }
        
        # Realiza la solicitud a la API de Serper
        response = requests.post(self.url, headers=headers, data=payload)
        
        if response.status_code != 200:
            return f"Error al obtener los resultados de búsqueda: {response.status_code}"

        # Analiza la respuesta
        results = response.json().get('organic', [])
        reddit_links = [result['link'] for result in results if 'reddit.com' in result['link']]

        if not reddit_links:
            return f"No se encontraron opiniones en Reddit para '{book_title}'"

        # Extrae opiniones de las páginas de Reddit
        opinions = []
        for link in reddit_links:
            opinion = self.scrape_reddit_page(link)
            if opinion:
                opinions.append(f"Desde: {link}\n{opinion}")

        return "\n\n".join(opinions) if opinions else f"No se encontraron opiniones en Reddit para '{book_title}'"

    def scrape_reddit_page(self, link: str) -> str:
        """Extrae opiniones de una página de Reddit."""
        try:
            # Realiza la solicitud a la página de Reddit
            reddit_response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            reddit_soup = BeautifulSoup(reddit_response.text, 'html.parser')
            
            # Extrae comentarios (ajusta según la estructura HTML actual de Reddit)
            comments = []
            for comment in reddit_soup.find_all('div', class_='md'):
                text = comment.get_text(strip=True)
                if text:
                    comments.append(text)
            
            return "\n".join(comments[:5]) if comments else "No se encontraron comentarios."
        except Exception as e:
            return f"Error al extraer la página: {str(e)}"
        

import json
import os

import requests
from langchain.tools import tool


class SearchTools():
    @staticmethod
    def search_book_recommendations(genre, person_1, person_2, person_3):
        """Useful to search for book recommendations in a specific genre by given people"""
        print(f"Searching for {genre} books recommended by {person_1}, {person_2}, and {person_3}...")
        top_result_to_return = 5
        url = "https://google.serper.dev/search"
        recommendations = []

        for person in [person_1, person_2, person_3]:
            query = f"{genre} books recommended by {person}"
            payload = json.dumps({"q": query, "num": top_result_to_return})
            headers = {
                'X-API-KEY': os.environ['SERPER_API_KEY'],
                'content-type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            if 'organic' not in response.json():
                print(f"No results found for {person}. There might be an error with your Serper API key.")
                continue

            results = response.json()['organic']
            print(f"Results for {person}:", results[:top_result_to_return])
            
            for result in results[:top_result_to_return]:
                try:
                    recommendations.append('\n'.join([
                        f"Recommender: {person}",
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue

        if not recommendations:
            return "Sorry, I couldn't find any book recommendations."
        else:
            return '\n'.join(recommendations)



# Script de prueba
if __name__ == "__main__":
    # Test RedditOpinionSearch
    print("Testing RedditOpinionSearch:")
    #reddit_searcher = RedditOpinionSearch()
    #book_title = "The Catcher in the Rye"
    #result = reddit_searcher.search_reddit_opinions(book_title)
    #print(result)

    # Test SearchTools
    print("\nTesting SearchTools:")
    search_tools = SearchTools()
    genre = "neuroscience"
    person_1 = "Elon Musk"
    person_2 = "Mark Zuckerberg"
    person_3 = "Lex Fridman"
    
    result = search_tools.search_book_recommendations(genre, person_1, person_2, person_3)
    print(result)