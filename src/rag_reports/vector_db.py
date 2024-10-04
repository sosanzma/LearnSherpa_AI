from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import DeepLake
from langchain_community.embeddings import OpenAIEmbeddings
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
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
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
        book_entries = re.split(r'####\s+\[?\d+\]?\.\s+\*\*', content)[1:]  # Skip the first empty split

        for i, entry in enumerate(book_entries, start=1):
            title_match = re.match(r'"(.*?)"\s+by\s+(.*?)\*\*', entry.strip())  # Match until next '**'
            if title_match:
                title = title_match.group(1).strip()
                author = title_match.group(2).strip()
                rating_match = re.search(r'\*\*Goodreads Rating\*\*:\s+([\d.]+)/5', entry)
                link_match = re.search(r'\[.*?\]\((https?://.*?)\)', entry)
                rating = rating_match.group(1) if rating_match else None
                # Updated summary_match to capture everything after **Summary:**
                summary_match = re.search(r'\*\*Summary:\*\*\s*\n(.*)', entry, re.DOTALL)                
                if summary_match:
                    summary = summary_match.group(1).strip()
                else:
                    summary = None

                metadata = {
                    "source": "goodreads",
                    "title": title,
                    "author": author,
                    "link": link_match.group(1) if link_match else None
                }

                # Create the formatted output for the current book
                formatted_entry = f"#### {i}. **\"{metadata['title']}\" by {metadata['author']}**\n"
                formatted_entry += f"- **Goodreads Rating:** {rating}/5\n"
                formatted_entry += f"- **Summary:** {summary}"


                # Append the processed entry to chunks
                chunks.append({"text": formatted_entry, "metadata": metadata})
        
        return chunks


    def process_reddit_report(self, content: str) -> List[Dict]:
        chunks = []
        # Split by the numbered entries like '1. **"Book Title"'
        book_entries = re.split(r'####\s+\[?\d+\]?\.\s+\*\*', content)[1:]  # Skip the first empty split

        for i, entry in enumerate(book_entries, start=1):
            # Match the book title and author within quotes
            title_match = re.match(r'"(.*?)"\s+by\s+(.*?)\*\*', entry.strip())
            if title_match:
                title = title_match.group(1).strip()
                author = title_match.group(2).strip()

                subreddit = re.findall( r'\*\*Subreddit:\*\*\s*([rR]/[\w\-]+)', entry, flags=re.IGNORECASE) 
                subreddit_links = re.findall(r'(https://www\.reddit\.com[^\)]+)\)\n', entry)
                # Updated summary_match to capture everything after **Summary:**
                summary_match = re.search(r'\*\*Summary:\*\*\s*\n(.*)', entry, re.DOTALL)                
                if summary_match:
                    summary = summary_match.group(1).strip()
                else:
                    summary = None
                metadata = {
                    "source": "reddit",
                    "title": title,
                    "author": author,
                    "subreddits": subreddit,
                    "link": subreddit_links
                }

                # Create the formatted output for the current book
                formatted_entry = f"#### {i}. **\"{metadata['title']}\" by {metadata['author']}**\n"
                if metadata['subreddits']:
                    formatted_entry += f"- **Subreddit:** r/{metadata['subreddits'][0]}\n"
                if metadata['link']:
                    formatted_entry += f"- **Link:** [Discussion]({metadata['link'][0]})\n"
                formatted_entry += f"- **Summary:** {summary}"


                # Append the processed entry to chunks
                chunks.append({"text": formatted_entry, "metadata": metadata})

        return chunks




    def add_reports(self, reports: Dict[str, str]):
        for report_type, content in reports.items():
            if report_type == "reddit":
                chunks = self.process_reddit_report(content)
            elif report_type == "goodreads":
                chunks = self.process_goodreads_report(content)
            else:
                print(f"Unknown report type: {report_type}")
                continue
            
            texts = [chunk["text"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            
            self.db.add_texts(texts, metadatas)
            print(f"Added {len(chunks)} chunks from {report_type} report to the database.")
            
            print("Chunks information:")
            for chunk in chunks:
                print(chunk)
            
            print("\n///////////////////////////\n")
            
            print("Metadata information:")
            for metadata in metadatas:
                print(metadata)


    def get_retriever(self):
        return self.db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 1}
        )
    def extract_book_title(self, text: str) -> str:
        match = re.search(r'"([^"]+)"', text)
        return match.group(1) if match else None