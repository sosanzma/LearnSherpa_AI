import json
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

class BookReviewTool:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.url = "https://google.serper.dev/search"

    def search_top_books(self, genre: str) -> list:
        query = f"top 3 best-selling {genre} books"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }

        print(f"Sending request to Serper API for genre: {genre}")
        print(f"Query: {query}")

        try:
            response = requests.post(self.url, headers=headers, data=payload)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return []

        data = response.json()
        print("Raw API response:")
        print(json.dumps(data, indent=2))

        if 'error' in data:
            print(f"API returned an error: {data['error']}")
            return []

        results = data.get('organic', [])
        print(f"Number of organic results: {len(results)}")

        books = []
        for result in results:
            snippet = result.get('snippet', '')
            print(f"Processing snippet: {snippet}")
            
            # Use regular expressions to find book titles and authors
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
                    print(f"Added book: {title} by {author}")

                if len(books) == 3:
                    break
            
            if len(books) == 3:
                break

        print(f"Found {len(books)} books for genre: {genre}")
        return books

def test_book_search():
    tool = BookReviewTool()
    genre = "self-improvment"
    print(f"\nTesting genre: {genre}")
    books = tool.search_top_books(genre)
    print("\nFinal results:")
    for i, book in enumerate(books, 1):
        print(f"Book {i}:")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Description: {book['description'][:100]}...")

if __name__ == "__main__":
    if not os.getenv('SERPER_API_KEY'):
        print("Error: SERPER_API_KEY not found in environment variables.")
    else:
        test_book_search()