import json
import os
import requests
import re
from bs4 import BeautifulSoup
from crewai_tools import BaseTool, tool

class BookReviewTool(BaseTool):
    name: str = "Book Review Tool"
    description: str = "A tool to find top-rated books in a specific genre and gather reviews and opinions."

    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.url = "https://google.serper.dev/search"

    def _run(self, genre: str) -> str:
        """Finds the top 3 books in a given genre and gathers reviews and opinions."""
        top_books = self.search_top_books(genre)
        results = []
        for book in top_books:
            reviews = self.get_book_reviews(book['title'], book['author'])
            results.append({
                'title': book['title'],
                'author': book['author'],
                'description': book['description'],
                'reviews': reviews
            })
        return json.dumps(results, indent=2)

    def search_top_books(self, genre: str) -> list:
        query = f"top 3 best-selling {genre} books"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }
        response = requests.post(self.url, headers=headers, data=payload)
        if response.status_code != 200:
            return []
        results = response.json().get('organic', [])
        books = []
        for result in results:
            snippet = result.get('snippet', '')
            matches = re.findall(r'([^·;]+?)(?:\s+by\s+|\s+[-—]\s+)([^·;]+)', snippet)
            for match in matches:
                title, author = match
                title = title.strip()
                author = author.strip()
                if title and author:
                    books.append({
                        'title': title,
                        'author': author,
                        'description': snippet
                    })
                if len(books) == 3:
                    break
            if len(books) == 3:
                break
        return books

    def get_book_reviews(self, title: str, author: str) -> list:
        query = f"{title} by {author} book reviews"
        payload = json.dumps({"q": query, "num": 3})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }
        response = requests.post(self.url, headers=headers, data=payload)
        if response.status_code != 200:
            return []
        results = response.json().get('organic', [])
        reviews = []
        for result in results:
            reviews.append({
                'source': result['title'],
                'snippet': result['snippet']
            })
        return reviews

