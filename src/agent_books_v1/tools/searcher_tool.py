import json
import os

import requests
from langchain.tools import tool


class SearchTools():

    @tool("Search for book recommendations")
    def search_book_recommendations(genre, person_1, person_2, person_3):
        """Useful to search for book recommendations in a specific genre by given people"""
        print(f"Searching for {genre} books recommended by {person_1}, {person_2}, and {person_3}...")
        top_result_to_return = 5
        url = "https://google.serper.dev/search"
        recommendations = []

        for person in [person_1, person_2, person_3]:
            query = f"neuroscience {genre} books recommended by {person}"
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
