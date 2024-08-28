import json
import os
import requests
from bs4 import BeautifulSoup
from crewai_tools import BaseTool, tool

class RedditOpinionSearch(BaseTool):
    name: str = "Reddit Opinion Search"
    description: str = "A tool to search for opinions about a specific book on Reddit using Serper."

    def __init__(self):
        # Ensure you have your Serper API key in environment variables
        self.api_key = os.getenv('SERPER_API_KEY')
        self.url = "https://google.serper.dev/search"
    
    @tool("Search for book opinions on Reddit")
    def search_reddit_opinions(self, book_title: str) -> str:
        """Searches for Reddit opinions on a specific book."""
        query = f"{book_title} book opinions site:reddit.com"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            'X-API-KEY': self.api_key,
            'content-type': 'application/json'
        }
        
        # Make the request to Serper API
        response = requests.post(self.url, headers=headers, data=payload)
        
        if response.status_code != 200:
            return f"Error fetching search results: {response.status_code}"

        # Parse the response
        results = response.json().get('organic', [])
        reddit_links = [result['link'] for result in results if 'reddit.com' in result['link']]

        if not reddit_links:
            return f"No Reddit opinions found for '{book_title}'"

        # Extract opinions from the Reddit pages
        opinions = []
        for link in reddit_links:
            opinion = self.scrape_reddit_page(link)
            if opinion:
                opinions.append(f"From: {link}\n{opinion}")

        return "\n\n".join(opinions) if opinions else f"No opinions found on Reddit for '{book_title}'"

    def scrape_reddit_page(self, link: str) -> str:
        """Scrapes opinions from a Reddit page."""
        try:
            # Make the request to the Reddit page
            reddit_response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            reddit_soup = BeautifulSoup(reddit_response.text, 'html.parser')
            
            # Extract comments (adjust based on Reddit's HTML structure)
            comments = []
            for comment in reddit_soup.find_all('div', class_='md'):
                text = comment.get_text(strip=True)
                if text:
                    comments.append(text)
            
            return "\n".join(comments[:5]) if comments else "No comments found."
        except Exception as e:
            return f"Error scraping page: {str(e)}"
