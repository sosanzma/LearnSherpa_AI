from crewai_tools import BaseTool
import praw

class RedditAPI(BaseTool):
    name: str = "Reddit Book Opinion API"
    description: str = (
        "A tool to fetch opinions about a specific book from Reddit discussions."
    )

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
            user_agent="YOUR_USER_AGENT"
        )

    def _run(self, book_title: str) -> str:
        subreddit = self.reddit.subreddit("books")
        search_query = f'title:"{book_title}"'
        opinions = []

        for post in subreddit.search(search_query, limit=5):
            opinions.append(f"Title: {post.title}")
            opinions.append(f"Opinion: {post.selftext[:200]}...")  # Truncate long posts
            
        return "\n\n".join(opinions) if opinions else f"No opinions found for '{book_title}'"


