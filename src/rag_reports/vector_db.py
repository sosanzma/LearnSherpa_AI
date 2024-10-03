from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import DeepLake
from langchain_openai import OpenAIEmbeddings as OpenAIEmbeddingsNew
import os
import re
from typing import Dict, List
from deeplake import delete

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['ACTIVELOOP_TOKEN'] = os.getenv("ACTIVELOOP_TOKEN")
ACTIVELOOP_ID = os.getenv("ACTIVELOOP_ID")

class VectorDB:
    def __init__(self, dataset_name, overwrite=False):
        self.embeddings = OpenAIEmbeddingsNew()
        self.dataset_path = f"hub://{ACTIVELOOP_ID}/{dataset_name}"
        
        if overwrite:
            self.recreate_db()
        else:
            self.db = DeepLake(dataset_path=self.dataset_path, embedding_function=self.embeddings, read_only=True)
        
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100) 
        self.book_metadata = {}  # New dictionary to store book metadata

    def recreate_db(self):
        try:
            delete(self.dataset_path)
            print(f"Remote dataset {self.dataset_path} has been deleted.")
        except Exception as e:
            print(f"Error deleting remote dataset: {str(e)}")
        
        self.db = DeepLake(dataset_path=self.dataset_path, embedding_function=self.embeddings, read_only=False)
        print(f"New dataset {self.dataset_path} has been created.")

    def process_goodreads_report(self, content: str):
        chunks = []
        # Split based on '#### X. **"Book Title" by Author**'
        book_entries = re.split(r'####\s+\d+\.\s+\*\*', content)[1:]  # Skip the first empty split

        for i, entry in enumerate(book_entries, start=1):
            title_match = re.match(r'"(.*?)"\s+by\s+(.*?)\*\*', entry.strip())  # Match until next '**'
            if title_match:
                title = title_match.group(1).strip()
                author = title_match.group(2).strip()
                rating_match = re.search(r'\*\*Goodreads Rating\*\*:\s+([\d.]+)/5', entry)
                link_match = re.search(r'\[.*?\]\((https?://.*?)\)', entry)
                summary_match = re.findall(r'- (.*?)\n', entry)  # Extract summary points

                metadata = {
                    "source": "goodreads",
                    "title": title,
                    "author": author,
                    "rating": rating_match.group(1) if rating_match else None,
                    "link": link_match.group(1) if link_match else None,
                    "summary": summary_match[:3]  # Limit to 3 summary points
                }

                # Create the formatted output for the current book
                formatted_entry = f"#### {i}. **\"{metadata['title']}\" by {metadata['author']}**\n"
                formatted_entry += f"- **Link:** [Goodreads Reviews]({metadata['link']})\n" if metadata['link'] else ""
                formatted_entry += f"- **Goodreads Rating:** {metadata['rating']}/5\n" if metadata['rating'] else ""
                formatted_entry += "- **Summary:**\n"
                for summary in metadata['summary']:
                    formatted_entry += f"  - {summary}\n"

                # Append the processed entry to chunks
                chunks.append({"text": formatted_entry, "metadata": metadata})
        
        return chunks


    def process_reddit_report(self, content: str) -> List[Dict]:
        chunks = []
        # Split by the numbered entries like '1. **"Book Title"'
        book_entries = re.split(r'\d+\.\s+\*\*', content)[1:]  # Skip the first empty split

        for i, entry in enumerate(book_entries, start=1):
            # Match the book title and author within quotes
            title_match = re.match(r'"(.*?)"\s+by\s+(.*?)\*\*', entry.strip())
            if title_match:
                title = title_match.group(1).strip()
                author = title_match.group(2).strip()

                # Extract Reddit discussion links
                subreddit_links = re.findall(r'\*\*Subreddit\*\*:\s+r/(\w+)\n- \*\*Link\*\*:\s+\[Discussion\]\((https?://.*?)\)', entry)
                summary_match = re.findall(r'- (.*?)\n', entry)  # Extract discussion summary points

                metadata = {
                    "source": "reddit",
                    "title": title,
                    "author": author,
                    "subreddits": [subreddit for subreddit, _ in subreddit_links],
                    "links": [link for _, link in subreddit_links],
                    "summary": summary_match[:3]  # Limit to 3 summary points
                }

                # Create the formatted output for the current book
                formatted_entry = f"#### {i}. **\"{metadata['title']}\" by {metadata['author']}**\n"
                if metadata['subreddits']:
                    formatted_entry += f"- **Subreddit:** r/{metadata['subreddits'][0]}\n"
                if metadata['links']:
                    formatted_entry += f"- **Link:** [Discussion]({metadata['links'][0]})\n"
                formatted_entry += "- **Summary:**\n"
                for summary in metadata['summary']:
                    formatted_entry += f"  - {summary}\n"

                # Append the processed entry to chunks
                chunks.append({"text": formatted_entry, "metadata": metadata})

        return chunks




    def add_reports(self, reports: Dict[str, str]):
        for report_type, content in reports.items():
            if report_type == "goodreads":
                chunks = self.process_goodreads_report(content)
            elif report_type == "reddit":
                chunks = self.process_reddit_report(content)
            else:
                print(f"Unknown report type: {report_type}")
                continue
            
            texts = [chunk["text"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            
            self.db.add_texts(texts, metadatas)
            print(f"Added {len(chunks)} chunks from {report_type} report to the database.")

    def get_retriever(self):
        return self.db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 1}
        )
    def extract_book_title(self, text: str) -> str:
        match = re.search(r'"([^"]+)"', text)
        return match.group(1) if match else None